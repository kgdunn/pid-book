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
  const boxes = labels.map((n) => n.renderedBoundingBox({ includeNodes: false, includeEdges: false, includeLabels: true }));
  let overlaps = 0;
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++) {
      const [a, b] = [boxes[i], boxes[j]];
      if (a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2) overlaps++;
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
  const open = async () => { await p.goto(ORIGIN, { waitUntil: "networkidle" }); await p.waitForTimeout(600); };
  await open();
  const box = await (await p.$("#cy")).boundingBox();
  const at = (pos) => [box.x + pos.x, box.y + pos.y];
  const topicAt = (id) => p.evaluate((i) => cy.getElementById(i).renderedPosition(), id);

  const verbs = await p.evaluate(() => [...new Set(DATA.edges.map((e) => e.type))].filter((v) => !(v in READ)));
  check(width, "every link verb has a reading", verbs.length === 0, verbs.join(", "));
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
  check(width, "its card quotes the book", (await p.textContent("#card blockquote cite")).includes(".rst:"));

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

  check(width, "no script errors", errors.length === 0, errors.join(" | "));
  await context.close();
}

const browser = await playwright().chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
});
try {
  await run(browser, 390, 844); // a phone
  await run(browser, 680, 1000); // a tablet in portrait
} finally {
  await browser.close();
}
console.log(failures.length ? `\n${failures.length} checks failed` : "\nall checks passed");
process.exit(failures.length ? 1 : 0);
