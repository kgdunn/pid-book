// node render.js page.html outdir [fps] [t1,t2,...]: every frame, or only the listed times (seconds) as stills
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [page_, outdir, fps_, only] = process.argv.slice(2);
  const fps = Number(fps_ || 30);
  fs.mkdirSync(outdir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(() => document.fonts.ready);
  if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
  const duration = await page.evaluate(() => window.DURATION);
  const times = only ? only.split(',').map(Number) : Array.from({ length: Math.round(duration * fps) }, (_, i) => i / fps);
  const canvas = page.locator('#c');
  for (const [i, t] of times.entries()) {
    await page.evaluate((t) => window.renderFrame(t), t);
    const name = only ? `still_${String(t).replace('.', '_')}.png` : `f_${String(i).padStart(5, '0')}.png`;
    await canvas.screenshot({ path: path.join(outdir, name) });
    if (errors.length) { console.error(`at t=${t}: ` + errors.join('\n')); process.exit(1); }
  }
  console.log(`${times.length} frames, ${duration}s at ${fps} fps`);
  await browser.close();
})();
