/*
 * "Run in browser" buttons under the book's Python examples.
 * Built by my-extensions/run_in_browser.py; Python runs in
 * run-in-browser-worker.js. Nothing loads until the reader clicks.
 *
 * A chapter is one linear script (the same contract CI checks), so clicking an
 * example first runs, once, every earlier example of the chapter that this tab
 * has not run yet, including those on earlier pages.
 */
(() => {
  "use strict";

  const STATIC = new URL("../", document.currentScript.src); // .../_static/
  const PLOTLY_CDN = (v) => `https://cdn.jsdelivr.net/npm/plotly.js-dist-min@${v}/plotly.min.js`;

  let worker = null;
  let nextId = 0;
  const waiting = new Map();
  const chapters = new Map(); // chapter -> Promise<manifest>
  const ran = new Map(); // chapter -> Set of block indices already run in this tab
  const preluded = new Set(); // pages whose prelude has run in this tab
  let busy = false;

  function getWorker(onStatus) {
    if (!worker) {
      worker = new Worker(new URL("js/run-in-browser-worker.js", STATIC), { type: "module" });
      worker.onmessage = ({ data }) => {
        if (data.status) return worker.onStatus?.(data.status);
        waiting.get(data.id)(data.result);
        waiting.delete(data.id);
      };
      // A worker that cannot start (Python not downloadable, say) answers nothing:
      // fail every waiting run instead of leaving its button on "Loading Python...".
      worker.onerror = (event) => {
        const error = `Could not start Python in this browser: ${event.message || "the download failed"}`;
        for (const resolve of waiting.values()) resolve({ stdout: "", error, figures: [] });
        waiting.clear();
        worker = null;
      };
    }
    worker.onStatus = onStatus;
    return worker;
  }

  /** Run a block of the chapter, or one statement of a plan on behalf of block ``index``. */
  function execute(manifest, index, onStatus, statement = null) {
    const block = manifest.blocks[index];
    const id = nextId++;
    return new Promise((resolve) => {
      waiting.set(id, resolve);
      getWorker(onStatus).postMessage({
        id,
        source: statement ?? block.source,
        filename: `${block.doc}.rst`,
        datasets: Object.fromEntries(
          Object.entries(manifest.datasets).map(([url, rel]) => [url, new URL(`run/${rel}`, STATIC).href]),
        ),
      });
    });
  }

  function manifest(chapter) {
    if (!chapters.has(chapter)) {
      chapters.set(chapter, fetch(new URL(`run/${chapter}.json`, STATIC)).then((r) => r.json()));
    }
    return chapters.get(chapter);
  }

  // ------------------------------------------------------------------ output
  // Whitespace is collapsed, and negative zero reads as zero: WebAssembly can round
  // a tiny value to -0.0 where the book, computed natively, printed 0.0.
  const normalise = (text) =>
    text
      .replace(/\s+/g, " ")
      .replace(/(^|[^\w.])-(0(?:\.0+)?)(?![\d.])/g, "$1$2")
      .trim();

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  let plotlyLoading = null;
  function loadPlotly(version) {
    plotlyLoading ??= new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = PLOTLY_CDN(version);
      s.onload = () => resolve(window.Plotly);
      s.onerror = reject;
      document.head.append(s);
    });
    return plotlyLoading;
  }

  async function render(out, block, result, note) {
    const parts = [];
    if (note) parts.push(el("p", "pid-run__note", note));
    if (result.stdout) parts.push(el("pre", "pid-run__stdout", result.stdout));
    if (result.error) parts.push(el("pre", "pid-run__error", result.error));

    // The book pins printed results in comments (# 0.255); say whether this run reproduced them.
    if (!result.error && block.expected.length) {
      const printed = normalise(result.stdout);
      const missing = block.expected.filter((line) => !printed.includes(normalise(line)));
      parts.push(
        missing.length
          ? el("p", "pid-run__check pid-run__check--differs", `Differs from the book: expected ${missing.join("; ")}`)
          : el("p", "pid-run__check", "✓ Matches the output in the book"),
      );
    }
    const plots = [];
    for (const fig of result.figures) {
      if (fig.kind === "png") {
        const img = el("img", "pid-run__figure");
        img.src = `data:image/png;base64,${fig.data}`;
        img.alt = "Figure produced by this example";
        parts.push(img);
      } else {
        const div = el("div", "pid-run__figure");
        parts.push(div);
        plots.push([div, JSON.parse(fig.json), fig.js]);
      }
    }
    if (!parts.length) parts.push(el("p", "pid-run__note", "Ran without printing anything."));
    out.replaceChildren(...parts);
    out.hidden = false;
    for (const [div, spec, version] of plots) {
      const Plotly = await loadPlotly(version);
      Plotly.newPlot(div, spec.data, { ...spec.layout, autosize: true }, { responsive: true, displaylogo: false });
    }
  }

  /** Say which earlier examples failed, linked to their pages. */
  function failedNote(blocks) {
    const p = el("p", "pid-run__note pid-run__error", "These earlier steps failed, so names they define may be missing: ");
    blocks.forEach((b, k) => {
      p.append(k ? "; " : "");
      if (b.statement) {
        p.append(el("code", "", b.statement), ` (${b.error.trim().split("\n").pop()})`);
        return;
      }
      const a = el("a", "", `${b.doc.split("/").pop()}, line ${b.line}`);
      a.href = new URL(`../${b.doc}`, STATIC).href;
      p.append(a);
    });
    return p;
  }

  // ------------------------------------------------------------------ click
  async function run(button) {
    if (busy) return;
    busy = true;
    const chapter = button.dataset.chapter;
    const index = Number(button.dataset.block);
    const out = button.nextElementSibling;
    const label = button.textContent;
    const status = (text) => {
      button.textContent = text.length > 60 ? `${text.slice(0, 57)}...` : text;
    };
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    try {
      status("Loading Python (first run only)...");
      const m = await manifest(chapter);
      if (!ran.has(chapter)) ran.set(chapter, new Set());
      const done = ran.get(chapter);

      // What this example needs first, in reading order (my-extensions/block_deps.py):
      // on the page's first click, the page's prelude (earlier examples, or single
      // statements: an import, a setting), run once so that it never undoes what a
      // later example set; then the page's own earlier examples. A manifest without
      // preludes means every earlier example.
      const doc = m.blocks[index].doc;
      const earlier = [...Array(index).keys()];
      const steps = !m.pages
        ? earlier
        : [...(preluded.has(doc) ? [] : m.pages[doc]), ...earlier.filter((i) => m.blocks[i].doc === doc)];
      preluded.add(doc);
      const plan = steps.filter(
        (step) => typeof step === "string" || (!m.blocks[step].skip && !done.has(step)),
      );
      const before = plan.filter((step) => typeof step === "number");
      const failed = [];
      for (const step of plan) {
        if (typeof step === "string") {
          const r = await execute(m, index, status, step);
          if (r.error) failed.push({ statement: step, error: r.error });
          continue;
        }
        status(`Running earlier example ${before.indexOf(step) + 1} of ${before.length}...`);
        const r = await execute(m, step, status);
        done.add(step);
        if (r.error) failed.push(m.blocks[step]);
      }
      status("Running...");
      const result = await execute(m, index, status);
      done.add(index);
      const notes = [];
      if (before.length) {
        notes.push(
          `First ran ${before.length} earlier example${before.length === 1 ? "" : "s"} of this chapter ` +
            "that this one builds on.",
        );
      }
      await render(out, m.blocks[index], result, notes.join(" "));
      if (failed.length) out.prepend(failedNote(failed));
    } catch (err) {
      out.replaceChildren(el("pre", "pid-run__error", `Could not run this example: ${err.message || err}`));
      out.hidden = false;
    } finally {
      button.textContent = label === "Run in browser" ? "Run again" : label;
      button.disabled = false;
      button.removeAttribute("aria-busy");
      busy = false;
    }
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest(".pid-run__button");
    if (button) run(button);
  });
})();
