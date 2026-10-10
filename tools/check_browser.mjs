#!/usr/bin/env node
// Click every "Run in browser" button of the built book in headless Chromium, as a
// reader would, and fail when one shows an error, prints something other than the book
// does, draws a figure that does not render, or never finishes.
//
// The Python checks (make check-code, make check-run-deps) run the examples in CPython.
// This runs them where readers do: Pyodide in a Web Worker, with packages from the
// Pyodide CDN and PyPI. It catches what only a browser shows: a package Pyodide does not
// ship, a worker the browser refuses to start, a Pyodide release whose scipy finds a
// different design. Python warnings printed in the browser are listed, not failed: they
// come from Pyodide's package versions, which CI's CPython does not have yet.
//
// Usage (after `make html`, or any HTML build of the book):
//
//   node tools/check_browser.mjs [--site _build/html] [--chapter NAME[,NAME]]...
//        [--changed FILE] [--jobs N] [--timeout SECONDS] [--report FILE.json] [--summary FILE.md]
//
// --changed takes a list of changed paths (git diff --name-only) and narrows the run to
// the chapters they touch, or keeps every chapter when the runner itself changed.
//
// Needs Playwright and its Chromium: npm install -g playwright && npx playwright install
// chromium. CHROMIUM_PATH points it at another Chromium; HTTPS_PROXY, when set, is used
// for everything but the local server.
import { execSync } from "node:child_process";
import { appendFileSync, existsSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { availableParallelism } from "node:os";
import { extname, join, resolve, sep } from "node:path";
import { parseArgs } from "node:util";

const { values: args } = parseArgs({
  options: {
    site: { type: "string", default: "_build/html" },
    chapter: { type: "string", multiple: true, default: [] },
    jobs: { type: "string", default: String(Math.min(4, availableParallelism())) },
    timeout: { type: "string", default: "300" },
    changed: { type: "string" },
    report: { type: "string" },
    summary: { type: "string" },
  },
});
const SITE = resolve(args.site);
// Paths that change how every button runs; any other change matters only to its chapter.
const RUNNER = [
  ".github/workflows/run-in-browser.yml", "_static/css/run-in-browser", "_static/js/run-in-browser",
  "conf.py", "my-extensions/block_deps.py", "my-extensions/run_in_browser.py",
  "tools/check_browser.mjs", "tools/check_code_blocks.py",
];
const WARNING = /\b([A-Z]\w*Warning): (.*)/;

// ------------------------------------------------------------ what to click
const RUN = join(SITE, "_static", "run");
if (!existsSync(RUN)) throw new Error(`${RUN} not found: build the book first (make html)`);
let manifests = readdirSync(RUN)
  .filter((f) => f.endsWith(".json"))
  .map((f) => JSON.parse(readFileSync(join(RUN, f), "utf-8")));
const named = args.chapter.flatMap((c) => c.split(",")).filter(Boolean);
const unknown = named.filter((c) => !manifests.some((m) => m.chapter === c));
if (!manifests.length || unknown.length) {
  throw new Error(`no buttons built for ${unknown.join(", ") || "any chapter"} in ${RUN}`);
}
if (named.length) manifests = manifests.filter((m) => named.includes(m.chapter));
if (args.changed) {
  const changed = readFileSync(args.changed, "utf-8").split("\n").filter(Boolean);
  if (!changed.some((path) => RUNNER.some((r) => path.startsWith(r)))) {
    manifests = manifests.filter((m) => changed.some((path) => path.startsWith(`${m.chapter}/`)));
  }
  if (!manifests.length) {
    const note = "### Run in browser: no chapter with buttons changed, nothing to click";
    console.log(note);
    if (args.summary) appendFileSync(args.summary, `${note}\n`);
    process.exit(0);
  }
}
const pages = manifests.flatMap((m) =>
  [...new Set(m.blocks.filter((b) => !b.skip).map((b) => b.doc))].map((doc) => ({ chapter: m.chapter, doc, m })),
);

// ------------------------------------------------------------ the site, served locally
// Pages are extensionless (conf.py: html_file_suffix = ""), so they go out as HTML.
const TYPES = {
  "": "text/html", ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript",
  ".css": "text/css", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml",
  ".csv": "text/csv", ".txt": "text/plain", ".woff2": "font/woff2", ".wasm": "application/wasm",
};
const server = createServer((req, res) => {
  const path = join(SITE, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (!(path + sep).startsWith(SITE + sep) || !existsSync(path) || statSync(path).isDirectory()) {
    res.writeHead(404).end();
    return;
  }
  res.writeHead(200, { "Content-Type": TYPES[extname(path)] ?? "application/octet-stream" });
  res.end(readFileSync(path));
});
await new Promise((ok) => server.listen(0, "127.0.0.1", ok));
const BASE = `http://127.0.0.1:${server.address().port}`;

// ------------------------------------------------------------ the browser
function playwright() {
  // A local install, else a global one (npm install -g playwright).
  for (const from of [import.meta.url, `${execSync("npm root -g").toString().trim()}/`]) {
    try {
      return createRequire(from)("playwright");
    } catch {}
  }
  throw new Error("Playwright is not installed: npm install -g playwright && npx playwright install chromium");
}
const browser = await playwright().chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  // Chromium sends even 127.0.0.1 to a proxy unless the bypass names it.
  proxy: process.env.HTTPS_PROXY
    ? { server: process.env.HTTPS_PROXY, bypass: "<-loopback>,localhost,127.0.0.1" }
    : undefined,
});
// One context: the pages share the browser's HTTP cache, so Pyodide downloads once.
const context = await browser.newContext();

async function checkPage({ doc, m }) {
  const page = await context.newPage();
  const problems = [];
  page.on("pageerror", (e) => e.message.includes("PagefindUI") || problems.push(`page error: ${e.message}`));
  const response = await page.goto(`${BASE}/${doc}`, { waitUntil: "domcontentloaded" });
  if (!response?.ok()) problems.push(`HTTP ${response?.status()} loading the page`);
  const buttons = page.locator(".pid-run__button");
  const results = [];
  const count = await buttons.count();
  // A page with fewer buttons than runnable examples must not pass by clicking nothing.
  const expected = m.blocks.filter((b) => b.doc === doc && !b.skip).length;
  if (count !== expected) problems.push(`${count} buttons on the page, ${expected} runnable examples in the manifest`);
  for (let k = 0; k < count; k++) {
    const button = buttons.nth(k);
    const block = m.blocks[Number(await button.getAttribute("data-block"))];
    const r = { label: `${block.doc}.rst:${block.line}`, status: "ok", check: "", errors: [], warnings: [] };
    const started = Date.now();
    // A DOM click: a pointer click can miss while the theme scrolls the sidebar.
    await button.evaluate((b) => b.click());
    try {
      const handle = await button.elementHandle();
      await page.waitForFunction((b) => b.textContent === "Run again", handle, { timeout: args.timeout * 1000 });
    } catch {
      r.status = "hung";
      r.why = `still "${await button.textContent()}" after ${args.timeout} s`;
      results.push({ ...r, seconds: (Date.now() - started) / 1000 });
      break; // the worker is busy for good; the page's later buttons would only queue
    }
    r.seconds = (Date.now() - started) / 1000;
    Object.assign(
      r,
      await button.locator("xpath=following-sibling::div[1]").evaluate((out) => ({
        errors: [...out.querySelectorAll(".pid-run__error")].map((e) => e.textContent.trim()),
        check: out.querySelector(".pid-run__check")?.textContent ?? "",
        stdout: out.querySelector(".pid-run__stdout")?.textContent ?? "",
        figures: out.querySelectorAll(".pid-run__figure").length,
        // Drawn: a Plotly chart rendered, or a matplotlib PNG that decoded.
        drawn:
          out.querySelectorAll(".pid-run__figure .plot-container").length +
          [...out.querySelectorAll("img.pid-run__figure")].filter((i) => i.naturalWidth > 0).length,
      })),
    );
    r.warnings = r.stdout.split("\n").flatMap((line) => line.match(WARNING)?.[0].slice(0, 160) ?? []);
    delete r.stdout;
    r.why = r.errors.at(-1)?.split("\n").at(-1) ?? (r.check.startsWith("Differs") ? r.check : "");
    if (r.drawn < r.figures) r.why ||= `${r.drawn} of ${r.figures} figures drew`;
    if (r.why) r.status = "fail";
    results.push(r);
  }
  await page.close();
  return { doc, problems, buttons: results };
}

// ------------------------------------------------------------ run, longest pages first
const started = Date.now();
const done = [];
const queue = [...pages].sort((a, b) => countOf(b) - countOf(a));
function countOf({ doc, m }) {
  return m.blocks.filter((b) => b.doc === doc && !b.skip).length;
}
await Promise.all(
  Array.from({ length: Number(args.jobs) }, async () => {
    for (let p = queue.shift(); p; p = queue.shift()) {
      // A crash on one page is that page's failure, not the end of the report.
      const result = { chapter: p.chapter, ...(await checkPage(p).catch((e) => ({ doc: p.doc, problems: [String(e)], buttons: [] }))) };
      done.push(result);
      const bad = result.buttons.filter((b) => b.status !== "ok").length + result.problems.length;
      const first = result.buttons[0]?.seconds ?? 0;
      console.log(`${bad ? "FAIL" : "ok  "} ${p.doc}: ${result.buttons.length} buttons, first click ${first.toFixed(1)} s`);
      for (const b of result.buttons.filter((b) => b.status !== "ok")) {
        console.log(`     ${b.status} ${b.label}: ${b.why}\n       ${b.errors.join("\n").replace(/\n/g, "\n       ")}`);
      }
      for (const problem of result.problems) console.log(`     ${problem}`);
    }
  }),
);
await browser.close();
server.close();

// ------------------------------------------------------------ report
const order = pages.map((p) => p.doc);
done.sort((a, b) => order.indexOf(a.doc) - order.indexOf(b.doc));
const all = done.flatMap((p) => p.buttons.map((b) => ({ ...b, chapter: p.chapter })));
const failing = all.filter((b) => b.status !== "ok");
const problems = done.flatMap((p) => p.problems.map((text) => `${p.doc}: ${text}`));
const pyodide = [...new Set(manifests.map((m) => m.pyodide))].join(", ");
const minutes = ((Date.now() - started) / 60000).toFixed(1);

const short = (doc) => doc.split("/").pop();
const rows = manifests.map(({ chapter }) => {
  const own = done.filter((p) => p.chapter === chapter);
  const buttons = own.flatMap((p) => p.buttons);
  const first = (p) => p?.buttons[0]?.seconds ?? 0;
  const slowest = own.reduce((s, p) => (first(p) > first(s) ? p : s), own[0]);
  return [
    chapter,
    own.length,
    buttons.length,
    buttons.filter((b) => b.check.startsWith("✓")).length,
    buttons.filter((b) => b.status !== "ok").length,
    buttons.reduce((n, b) => n + b.warnings.length, 0),
    slowest ? `${first(slowest).toFixed(0)} s, ${short(slowest.doc)}` : "",
  ];
});
const md = [
  `### Run in browser, Pyodide ${pyodide}: ${failing.length + problems.length ? "❌" : "✅"} ` +
    `${all.length} buttons on ${done.length} pages, ${failing.length} failing (${minutes} min)`,
  "",
  "| Chapter | Pages | Buttons | Match the book | Failing | Python warnings | Slowest first click |",
  "|---|---:|---:|---:|---:|---:|---|",
  ...rows.map((r) => `| ${r.join(" | ")} |`),
  "",
  ...(failing.length || problems.length
    ? ["**Failing**", "", ...failing.map((b) => `- \`${b.label}\` (${b.status}): ${b.why}`), ...problems.map((p) => `- ${p}`), ""]
    : []),
  ...(all.some((b) => b.warnings.length)
    ? ["**Python warnings a reader sees** (listed, not failed: they come from Pyodide's package versions)", "",
       ...all.flatMap((b) => b.warnings.map((w) => `- \`${b.label}\`: ${w}`)), ""]
    : []),
].join("\n");

console.log(`\n${md}`);
if (args.summary) appendFileSync(args.summary, `${md}\n`);
if (args.report) writeFileSync(args.report, JSON.stringify({ pyodide, pages: done }, null, 1));
process.exit(failing.length || problems.length ? 1 : 0);
