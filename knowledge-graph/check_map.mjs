#!/usr/bin/env node
// Drive the knowledge-graph map in headless Chromium, as a reader would on a phone and a tablet,
// and fail when it misbehaves: a script error, a page that scrolls sideways, a topic or term that
// a tap does not open, a drag that does not pan, labels that overlap or stop growing as you zoom,
// or a switch (term names, kinds of term) that does not do what it says or is not remembered.
//
// Usage (after layout_kg.py has written the page):
//
//   node knowledge-graph/check_map.mjs [path/to/experimental-design-graph.html]
//
// Needs Playwright and its Chromium, as tools/check_browser.mjs does. The page loads Cytoscape and
// its fonts from CDNs, so it needs the network; HTTPS_PROXY, when set, is used.
import { execSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const page = process.argv[2] || join(here, "experimental-design-graph.html");
const html = "<!doctype html>" + readFileSync(page, "utf8");
const ORIGIN = "https://map.test/"; // a real origin, so the page's localStorage works

function playwright() {
  for (const from of [import.meta.url, `${execSync("npm root -g").toString().trim()}/`]) {
    try {
      return createRequire(from)("playwright");
    } catch {}
  }
  throw new Error("Playwright is not installed: npm install -g playwright && npx playwright install chromium");
}

const failures = [];
const check = (width, name, ok, detail = "") => {
  console.log(`${ok ? "ok  " : "FAIL"} ${width}px  ${name}${detail ? `: ${detail}` : ""}`);
  if (!ok) failures.push(`${width}px ${name}`);
};

// Everything the checks read comes from the page's own globals (cy, DATA, READ).
const state = (p) => p.evaluate(() => {
  const labels = cy.nodes(".term.lab");
  const box = (n) => n.renderedBoundingBox({ includeNodes: false, includeEdges: false, includeLabels: true });
  const hit = (a, b) => a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2;
  const boxes = labels.map(box);
  // Topic and sub-topic names count too: a term's name must not cover them.
  const names = cy.nodes(".topic, .subtopic, .subname").filter((n) => n.visible() && n.style("label")).map(box);
  let overlaps = 0;
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) if (hit(boxes[i], boxes[j])) overlaps++;
    for (const g of names) if (hit(boxes[i], g)) overlaps++;
  }
  return {
    zoom: cy.zoom(), pan: { ...cy.pan() }, labels: labels.length, overlaps,
    font: labels.length ? parseFloat(labels[0].renderedStyle("font-size")) : 0,
    terms: cy.nodes(".term").filter((n) => n.visible()).length,
    links: cy.edges(".link").filter((e) => e.visible()).length,
  };
});

async function run(browser, width, height) {
  const context = await browser.newContext({ viewport: { width, height }, colorScheme: "dark" });
  const p = await context.newPage();
  const errors = [];
  p.on("pageerror", (e) => errors.push(e.message));
  p.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await p.route(ORIGIN, (r) => r.fulfill({ contentType: "text/html", body: html }));
  // Wait for the map itself, not for the network to fall quiet: the font CDN can keep a connection open.
  const open = async () => {
    await p.goto(ORIGIN, { waitUntil: "load" });
    await p.waitForFunction(() => typeof cy !== "undefined" && cy.nodes().length > 0, null, { timeout: 30000 });
    await p.waitForTimeout(600);
  };
  await open();
  const box = await (await p.$("#cy")).boundingBox();
  const at = (pos) => [box.x + pos.x, box.y + pos.y];
  const topicAt = (id) => p.evaluate((i) => cy.getElementById(i).renderedPosition(), id);

  const verbs = await p.evaluate(() => [...new Set(DATA.edges.map((e) => e.type))].filter((v) => !(v in READ)));
  check(width, "every link verb has a reading", verbs.length === 0, verbs.join(", "));
  const how = await p.textContent("#how");
  const n = await p.evaluate(() => DATA.edges.length);
  check(width, "the explanation is filled from the map's data", how.includes(`${n} links`) && !/undefined|NaN/.test(how));
  const guide = await p.evaluate(() => ({ steps: document.querySelectorAll("#how details.guide ol > li").length,
    folder: [...document.querySelectorAll("#how details.guide a")].find((a) => a.textContent.includes("folder"))?.href }));
  check(width, "the step-by-step guide links the code's folder", guide.steps === 7
    && guide.folder === "https://github.com/kgdunn/pid-book/tree/main/knowledge-graph", guide.folder);
  check(width, "the explanation draws each kind of term in its legend shape",
    (await p.evaluate(() => document.querySelectorAll("#how .kind svg path").length)) === 5);
  const told = await p.evaluate(() => [...document.querySelectorAll("#how > p, #how > ul")].map((e) => e.textContent).join(" "));
  check(width, "the explanation is in words until 'Show the numbers' is opened", !/\d/.test(told), told.match(/\S*\d\S*/g)?.join(" "));
  const page = await p.evaluate(() => {
    // In DejaVu Sans, wider than any phone's own font, so two lines here are two lines on any phone.
    const lede = document.querySelector("header .sub"); lede.style.fontFamily = '"DejaVu Sans", sans-serif';
    const sub = document.createRange(); sub.selectNodeContents(lede);
    return { subLines: new Set([...sub.getClientRects()].map((r) => Math.round(r.top))).size,
      words: document.body.textContent + DATA.nodes.map((n) => n.definition).join(" "),
      examples: document.querySelector('#legend button[data-fam="context"]').getAttribute("aria-pressed"),
      code: document.getElementById("code").href };
  });
  check(width, "the subtitle fits on two lines", page.subLines <= 2, `${page.subLines} lines`);
  check(width, "no 'teach' or 'taught' on the page", !/\bteach|\btaught/i.test(page.words));
  check(width, "examples, questions and sources start hidden", page.examples === "false");
  check(width, "the footer links the clustering code", page.code.startsWith("https://github.com/kgdunn/pid-book/blob/"));
  check(width, "no sideways scroll", (await p.evaluate(() => document.documentElement.scrollWidth)) <= width);
  check(width, "opens on the topics, terms hidden", (await state(p)).terms === 0);

  // A drag that starts on a topic circle pans the map (the circles cover most of it).
  const big = await p.evaluate(() => DATA.clusters[0].id);
  const before = (await state(p)).pan;
  const [x, y] = at(await topicAt(big));
  await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.move(x + 50, y + 30, { steps: 6 }); await p.mouse.up();
  const after = (await state(p)).pan;
  check(width, "a drag on a topic pans", Math.abs(after.x - before.x) > 20 && Math.abs(after.y - before.y) > 10);

  // A tap inside a topic opens it.
  await p.click("#home"); await p.waitForTimeout(500);
  const [tx, ty] = at(await topicAt(big));
  await p.mouse.click(tx, ty); await p.waitForTimeout(700);
  const topicName = await p.evaluate((i) => DATA.clusters.find((c) => c.id === i).name, big);
  check(width, "a tap opens the topic", (await p.textContent("#card h2")) === topicName);

  // Inside a topic with a second level: its sub-topics are drawn, and while their names sit in their
  // middle, they stand for their terms (no term is named).
  const inner = await p.evaluate((i) => {
    const subs = DATA.clusters.find((c) => c.id === i).subs;
    const drawn = subs.filter((s) => cy.getElementById(s.id).visible()).length;
    const gap = 62 * cy.zoom();   // TERM_GAP: the on-screen distance between neighbouring terms
    const named = cy.nodes(".term.lab").filter((n) => n.data("topic") === i).length;
    return { subs: subs.length, drawn, gap, named };
  }, big);
  check(width, "its sub-topics are drawn", inner.subs > 1 && inner.drawn === inner.subs, `${inner.drawn} of ${inner.subs}`);
  if (inner.gap < 45) check(width, "sub-topic names stand for their terms", inner.named === 0, `${inner.named} terms named`);

  // A tap inside a sub-topic, clear of its terms, opens it.
  const spot = await p.evaluate((i) => {
    const s = DATA.clusters.find((c) => c.id === i).subs[0];
    const node = cy.getElementById(s.id), c = node.renderedPosition(), r = node.renderedWidth() / 2;
    const dots = cy.nodes(".term").filter((n) => n.visible()).map((n) => n.renderedPosition());
    for (let f = 0; f <= 0.8; f += 0.1)
      for (let a = 0; a < 2 * Math.PI; a += Math.PI / 8) {
        const x = c.x + f * r * Math.cos(a), y = c.y + f * r * Math.sin(a);
        if (x > 5 && y > 5 && x < cy.width() - 5 && y < cy.height() - 5 && dots.every((d) => Math.hypot(d.x - x, d.y - y) > 16))
          return { x, y, name: s.name };
      }
    return null;
  }, big);
  if (spot) {
    await p.mouse.click(box.x + spot.x, box.y + spot.y); await p.waitForTimeout(700);
    check(width, "a tap opens the sub-topic", (await p.textContent("#card h2")) === spot.name, spot.name);
  } else check(width, "a tap opens the sub-topic", false, "no clear spot to tap");

  // Zooming in: labels never overlap, and grow up to their cap.
  const fonts = [];
  for (let step = 0; step < 3; step++) {
    const s = await state(p);
    check(width, `zoom step ${step}: no label overlaps`, s.overlaps === 0, `${s.overlaps} of ${s.labels}`);
    fonts.push(s.font);
    await p.click("#zin"); await p.waitForTimeout(500);
  }
  check(width, "labels grow as you zoom in", fonts.every((f, i) => i === 0 || f > fonts[i - 1] || f >= 19),
        fonts.map((f) => f.toFixed(1)).join(" -> "));

  // A tap on a term opens it and lights up its links.
  const term = await p.evaluate(() => cy.nodes(".term").filter((n) => n.visible() && n.renderedPosition().x > 40
    && n.renderedPosition().x < cy.width() - 40 && n.renderedPosition().y > 40 && n.renderedPosition().y < cy.height() - 40)[0].id());
  const [ux, uy] = at(await p.evaluate((i) => cy.getElementById(i).renderedPosition(), term));
  await p.mouse.click(ux, uy); await p.waitForTimeout(700);
  const lit = await p.evaluate((i) => ({ hl: cy.edges(".link.hl").length, degree: cy.getElementById(i).connectedEdges(".link").length,
    name: DATA.nodes.find((n) => n.id === i).name }), term);
  check(width, "a tap opens the term", (await p.textContent("#card h2")) === lit.name, lit.name);
  check(width, "its links light up", lit.hl === lit.degree, `${lit.hl} of ${lit.degree}`);
  const card = await p.textContent("#card");
  check(width, "its card quotes the book, not its source file", (await p.textContent("#card blockquote")).trim().length > 0 && !card.includes(".rst"));

  // The term-name switch: off names only the selected term, and is remembered.
  await p.click("#labels"); await p.waitForTimeout(300);
  check(width, "names off: only the selected term is named", (await state(p)).labels === 1);
  await open();
  check(width, "names off is remembered", (await p.getAttribute("#labels", "aria-pressed")) === "false");
  await p.click("#labels");

  // The kind switches: hiding concepts removes them and their links, keeps a selected one, is remembered.
  await p.click('.chip[data-id="c0"]'); await p.waitForTimeout(700);
  const all = await state(p);
  await p.click('#legend button[data-fam="concept"]'); await p.waitForTimeout(300);
  const fewer = await state(p);
  const concepts = await p.evaluate(() => cy.nodes(".term").filter((n) => n.data("fam") === "concept" && n.visible()).length);
  check(width, "hiding concepts removes them and their links", concepts === 0 && fewer.links < all.links,
        `${all.terms} -> ${fewer.terms} terms, ${all.links} -> ${fewer.links} links`);
  const concept = await p.evaluate(() => DATA.nodes.find((n) => n.type === "Concept").id);
  await p.evaluate((i) => { location.hash = i.replaceAll("_", "-"); }, concept); await p.waitForTimeout(600);
  check(width, "a selected concept stays visible", await p.evaluate((i) => cy.getElementById(i).visible(), concept));
  await open();
  check(width, "hidden kinds are remembered",
        (await p.getAttribute('#legend button[data-fam="concept"]', "aria-pressed")) === "false");
  await p.click('#legend button[data-fam="concept"]');

  // Each topic and sub-topic shows its number of terms, in square brackets on a second line.
  const counted = await p.evaluate(() => DATA.clusters.every((c) => cy.getElementById(c.id).data("olabel") === `${c.short}\n[${c.size}]`
    && (c.subs || []).every((s) => cy.getElementById(`${s.id}-name`).data("label") === `${s.name}\n[${s.size}]`)));
  check(width, "topics and sub-topics show their number of terms", counted);

  // The colour mode: three presses go through light, dark and back to the system's (dark here); the map
  // redraws in the page's colours, and a chosen mode is kept.
  const look = () => p.evaluate(() => ({ theme: document.documentElement.dataset.theme || "auto",
    text: cy.nodes(".topic")[0].style("color") }));
  const modes = [await look()];
  for (let i = 0; i < 3; i++) { await p.click("#mode"); await p.waitForTimeout(200); modes.push(await look()); }
  check(width, "the mode switch goes light, dark, then the system's",
        modes.map((m) => m.theme).join(" ") === "auto light dark auto", modes.map((m) => m.theme).join(" "));
  check(width, "the map redraws in the chosen mode", modes[1].text !== modes[2].text && modes[2].text === modes[3].text);
  await p.click("#mode"); await open();
  check(width, "the colour mode is kept", (await look()).theme === "light");

  check(width, "no script errors", errors.length === 0, errors.join(" | "));
  await context.close();
}

// On a touch screen one finger scrolls the page and leaves the map, with no tap on lifting; a hiding toolbar (a taller
// window) keeps the view; two fingers move the map, and spreading them zooms in.
async function fingerScrolls(browser) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true });
  const p = await context.newPage();
  const errors = [];
  p.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await p.route(ORIGIN, (r) => r.fulfill({ contentType: "text/html", body: html }));
  await p.goto(ORIGIN, { waitUntil: "load" });
  await p.waitForFunction(() => typeof cy !== "undefined" && cy.nodes().length > 0, null, { timeout: 30000 });
  await p.waitForTimeout(600);
  const finger = await context.newCDPSession(p);
  const touch = (type, points) => finger.send("Input.dispatchTouchEvent", { type, touchPoints: points });
  const drag = async (rise, fingers = 1) => {
    const box = await (await p.$("#cy")).boundingBox();
    const xs = Array.from({ length: fingers }, (_, k) => box.x + box.width * (k + 1) / (fingers + 1));
    const y = box.y + 0.8 * box.height;
    const at = (dy) => xs.map((x, id) => ({ x, y: y - dy, id }));
    await touch("touchStart", at(0));
    for (let step = 1; step <= rise / 15; step++) await touch("touchMove", at(15 * step));
    await touch("touchEnd", []);
    await p.waitForTimeout(800);
  };
  const view = () => p.evaluate(() => ({ scrolled: scrollY, title: document.querySelector("#card h2").textContent,
    pan: JSON.stringify([cy.pan(), cy.zoom()]), y: cy.pan().y, zoom: cy.zoom() }));
  const before = await view();
  await drag(300);
  const after = await view();
  check(390, "one finger scrolls the page and leaves the map",
    after.scrolled > before.scrolled + 100 && after.pan === before.pan && after.title === before.title,
    `scrolled ${after.scrolled - before.scrolled} px`);
  await p.setViewportSize({ width: 390, height: 900 }); await p.waitForTimeout(500);
  const kept = await view();
  check(390, "a toolbar hiding keeps the view", kept.pan === after.pan);
  await p.evaluate(() => window.scrollTo(0, 0));
  await drag(150, 2);
  const moved = await view();
  check(390, "two fingers move the map and leave the page", moved.y < kept.y - 50 && moved.scrolled === 0);
  const box = await (await p.$("#cy")).boundingBox();
  const [cx, cyy] = [box.x + box.width / 2, box.y + box.height / 2];
  for (let k = 0; k <= 8; k++) {
    const apart = 30 + 10 * k;
    await touch(k ? "touchMove" : "touchStart", [{ x: cx - apart, y: cyy, id: 0 }, { x: cx + apart, y: cyy, id: 1 }]);
  }
  await touch("touchEnd", []);
  await p.waitForTimeout(600);
  check(390, "spreading two fingers zooms in", (await view()).zoom > moved.zoom * 1.5);
  check(390, "no console errors from touch", errors.length === 0, errors.join(" | "));
  await context.close();
}

const browser = await playwright().chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
});
try {
  await run(browser, 390, 844); // a phone
  await fingerScrolls(browser);
  await run(browser, 680, 1000); // a tablet in portrait
} finally {
  await browser.close();
}
console.log(failures.length ? `\n${failures.length} checks failed` : "\nall checks passed");
process.exit(failures.length ? 1 : 0);
