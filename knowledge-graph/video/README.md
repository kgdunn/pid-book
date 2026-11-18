# A video of the concept map

A short video drawn from the map file itself, `../doe_kg_map.json`: the map builds itself, the two
other texts sweep across it, it opens one topic and one of its sub-topics, and four links are read
out as sentences. It was made for a post about the map at <https://factori.al/map/>.

Only the scripts are kept here. The page, the frames and the video are made from them, and git
ignores all three.

| File | What it does |
|---|---|
| `build_page.py` | Sets the map's data into `template.html` and writes `page.html`. It also checks the dive. |
| `template.html` | Draws any moment of the video on a canvas: `window.renderFrame(t)`, `t` in seconds. It reads no clock. |
| `render.js` | Opens `page.html` in Chromium and saves one PNG for each frame. |

## Make it

Build the graph first (see [`../README.md`](../README.md)), then from this folder:

```bash
python -I build_page.py
node render.js page.html frames
ffmpeg -framerate 30 -i frames/f_%05d.png -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p \
  -movflags +faststart out/concept-map.mp4
```

The video is 1080 by 1350 pixels and 50 seconds long, at 30 frames a second: 1494 frames, which
take about three minutes to draw.

It needs Python 3 (no packages), Node.js with [Playwright](https://playwright.dev/) and its Chromium
(`npm install playwright`, then `npx playwright install chromium`), and ffmpeg. The words are set in
Inter where the computer has it, and in the system's own font where it does not.

## Change it

- **Speed.** `python -I build_page.py --slow 1.5`. The times in `template.html` are those of the
  first cut, which moved on before its words could be read; `--slow` stretches them all, and 2 is
  the default.
- **Theme.** `python -I build_page.py --theme dark`.
- **A still.** `node render.js page.html stills 30 12,31.5` saves the frames at 12 and 31.5
  seconds only, to look at one moment without drawing them all.
- **The dive.** `DIVE` at the top of `build_page.py` names the topic, the sub-topic and the four
  links that are read out. The four must differ in who else states them: no other text, the first,
  the second, both. When the graph changes and they no longer do, `build_page.py` stops and lists
  the sub-topic's links with who states each, to choose from.
- **The words on screen** are in `template.html`: the headings in `TITLES`, and the lines of the
  panel under the map.

## What it shows of the other texts

A link is drawn in a text's colour when `graph.yaml` records that the text also states it, and in
black when both do. Links between two topics are drawn faint and thin, because drawn as strongly as
the links inside a topic they crossed the whole map and hid it. The live map shows the same
comparison another way, as a ring on each topic and each term.
