"""Render one built book page into a single self-contained HTML file for proofreading.

The page is taken from ``_build/html``, so whatever this produces is exactly what
Sphinx produced from the RST: there is no second copy of the prose to drift out of
step. Images are inlined as data URIs and the theme chrome (navigation, sidebars,
search) is dropped, leaving the article body on a plain reading page.

Run ``make html`` first, then::

    python tools/sync_proof_artifact.py <docname> [output.html]

``docname`` is the path under ``_build/html`` without any extension, for example
``latent-variable-modelling/projection-to-latent-structures/pls-model-inversion-and-the-orthogonal-space``.
Output defaults to ``_build/proof/<basename>.html``.
"""

from __future__ import annotations

import base64
import mimetypes
import re
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent / "_build" / "html"

# Reading styles for the standalone page. Deliberately close to the book's own
# proportions so that line breaks and paragraph rhythm proofread the same way.
STYLE = """
:root{
  --blue:#1f3d7a; --amber:#e6820a; --maroon:#7b1d2b;
  --paper:#fcfcfd; --raised:#f2f4f8; --ink:#12151c; --muted:#5b6478; --rule:#d9dee7;
  --code:#f3f5fa;
  --serif:"Charter","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:"Avenir Next","Segoe UI",system-ui,-apple-system,sans-serif;
  --mono:"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0e1117; --raised:#171b24; --ink:#e4e7ee; --muted:#98a1b4; --rule:#2a303c;
  --code:#151922; --blue:#8fb0ea; --amber:#f0a03c; --maroon:#e08496;}}
:root[data-theme="dark"]{
  --paper:#0e1117; --raised:#171b24; --ink:#e4e7ee; --muted:#98a1b4; --rule:#2a303c;
  --code:#151922; --blue:#8fb0ea; --amber:#f0a03c; --maroon:#e08496;}
:root[data-theme="light"]{
  --paper:#fcfcfd; --raised:#f2f4f8; --ink:#12151c; --muted:#5b6478; --rule:#d9dee7;
  --code:#f3f5fa; --blue:#1f3d7a; --amber:#e6820a; --maroon:#7b1d2b;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);
     font-size:17.5px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:52rem;margin:0 auto;padding:2.4rem 1.4rem 6rem}
.banner{font-family:var(--sans);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:600;border-bottom:2px solid var(--rule);
  padding-bottom:.8rem;margin-bottom:2rem}
h1{font-size:2rem;line-height:1.18;font-weight:600;margin:0 0 1.2rem;text-wrap:balance}
h2{font-size:1.32rem;font-weight:600;margin:2.6rem 0 .8rem;padding-top:1rem;
   border-top:1px solid var(--rule);text-wrap:balance}
h3{font-size:1.12rem;font-weight:600;margin:2rem 0 .6rem;color:var(--blue)}
h4,h5{font-size:1rem;font-weight:600;margin:1.6rem 0 .5rem}
p{margin:0 0 1rem}
a{color:var(--blue)}
figure{margin:1.8rem 0}
img{max-width:100%;height:auto;display:block;border:1px solid var(--rule);
    border-radius:4px;background:#fff}
figcaption,.caption{font-family:var(--sans);font-size:.79rem;line-height:1.5;
  color:var(--muted);margin-top:.6rem}
pre{font-family:var(--mono);font-size:.8rem;line-height:1.55;background:var(--code);
  border:1px solid var(--rule);border-radius:5px;padding:.85rem 1rem;overflow-x:auto;margin:1.2rem 0}
code{font-family:var(--mono);font-size:.87em;background:var(--code);padding:.08em .3em;border-radius:3px}
pre code{background:none;padding:0}
.table-wrap,.table-responsive{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-family:var(--sans);font-size:.8rem;
  font-variant-numeric:tabular-nums;margin:1.4rem 0}
caption{font-family:var(--sans);font-size:.78rem;color:var(--muted);text-align:left;
  padding:.7rem .2rem;line-height:1.45}
th,td{padding:.45rem .8rem;text-align:right;border-bottom:1px solid var(--rule);white-space:nowrap}
th:first-child,td:first-child{text-align:left}
thead th{background:var(--raised);font-weight:600;color:var(--blue)}
.headerlink{display:none}
:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
"""

# Theme furniture that carries no prose: strip it so the page reads as an article.
DROP_SELECTORS = (
    "sphinx-tabs",
    "prev-next",
    "bd-sidebar",
    "bd-header",
    "bd-footer",
    "searchbox",
    "toc-item",
)


def inline_images(html: str, page: Path) -> tuple[str, int]:
    """Replace every ``src`` with a base64 data URI so the file stands alone."""
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        src = match.group(2)
        if src.startswith("data:"):
            return match.group(0)
        target = (page.parent / src).resolve()
        if not target.is_file():
            return match.group(0)
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        payload = base64.b64encode(target.read_bytes()).decode("ascii")
        count += 1
        return f'{match.group(1)}"data:{mime};base64,{payload}"'

    html = re.sub(r'(<img[^>]*\ssrc=)"([^"]+)"', repl, html)
    return html, count


def extract_article(html: str) -> str:
    """Return the ``<article class="bd-article">`` body, without its wrapper tag."""
    start = html.find('<article class="bd-article">')
    if start == -1:
        msg = "no <article class='bd-article'> found; did the theme change?"
        raise SystemExit(msg)
    open_len = len('<article class="bd-article">')
    depth, i = 1, start + open_len
    for match in re.finditer(r"</?article\b", html[start + open_len :]):
        depth += 1 if match.group(0) == "<article" else -1
        if depth == 0:
            i = start + open_len + match.start()
            break
    return html[start + open_len : i]


def scrub(body: str) -> str:
    """Drop the logo/PDF badge images and the anchor-link pilcrows."""
    body = re.sub(r'<a class="headerlink".*?</a>', "", body, flags=re.S)
    body = re.sub(r"<img[^>]*(textbook-logo|Document-pdf)[^>]*>", "", body)
    return re.sub(r"<p>\s*</p>", "", body)


def main() -> None:
    """Render the named docname into a self-contained proofreading page."""
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    docname = sys.argv[1].removesuffix(".html")
    page = BUILD / docname
    if not page.is_file():
        msg = f"{page} not found; run `make html` first"
        raise SystemExit(msg)

    raw = page.read_text(encoding="utf-8")
    body = scrub(extract_article(raw))
    body, n_images = inline_images(body, page)

    title_match = re.search(r"<title>(.*?)</title>", raw, re.S)
    title = title_match.group(1).split("&#8212;")[0].strip() if title_match else docname

    out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        BUILD.parent / "proof" / f"{Path(docname).name}.html"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"<title>{title}</title>\n<style>{STYLE}</style>\n"
        f'<div class="wrap">\n'
        f'<div class="banner">Process Improvement using Data '
        f"&middot; proof copy, generated from the Sphinx build</div>\n"
        f"{body}\n</div>\n",
        encoding="utf-8",
    )
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB, {n_images} images inlined)")


if __name__ == "__main__":
    main()
