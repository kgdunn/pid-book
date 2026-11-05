"""Draw the README banner and a link-preview card per chapter, from the book's own examples.

Run from the repo root, with a Chrome or Chromium for plotly's image renderer:

    BROWSER_PATH=/path/to/chrome uv run --with 'process-improve[all]' --with kaleido \
        --with matplotlib python scripts/render_chapter_images.py

For each of chapters 1 to 6, the chapter's examples run in reading order, as
``tools/check_code_blocks.py`` runs them in CI, until the example named in ``EXAMPLES`` has
run; the figure that example shows is kept. kaleido (plotly's own renderer) draws it, so each
picture is the one a reader gets by clicking Run in browser under that example.

Writes:

* ``_static/banner-light.png`` and ``_static/banner-dark.png``: the banner at the top of the
  README and of the book's landing page, one tile per chapter.
* ``_static/social/<chapter>.png``: the card a shared link to a page of that chapter shows,
  set in ``conf.py`` (``social_meta_chapter_images``).
"""

from __future__ import annotations

import io
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "scripts")]

import check_code_blocks as ccb  # noqa: E402 (needs the path above)
from render_hero import (  # noqa: E402 (shares the social card's look)
    ACCENT,
    BG,
    CARD,
    INK,
    LINK,
    SANS,
    SANS_BOLD,
    SERIF,
    SUBINK,
    box,
    play_icon,
)

STATIC = ROOT / "_static"
DPI = 100
NAVY, NAVY_INK, NAVY_SUBINK = "#0F1B2A", "#F4EFE4", "#B9C3CE"  # the dark banner


@dataclass(frozen=True)
class Example:
    chapter: str  # the chapter's directory
    number: int
    title: str  # as the book's table of contents gives it
    file: str  # the RST file holding the example
    snippet: str  # text that only this example's code contains
    figure: int  # which of the figures the example shows (1 = first)
    caption: str


EXAMPLES = [
    Example("data-visualization", 1, "Visualizing Process Data", "data-visualization/box-plots.rst",
            "raincloud(stacked", 1, "Raincloud plot of board thickness at six positions"),
    Example("univariate-review", 2, "Univariate Data Analysis",
            "univariate-review/normal-distribution-and-checking-for-normality.rst",
            "Throw N six-sided dice", 1, "Averages of dice throws approach a normal distribution"),
    Example("process-monitoring", 3, "Process Monitoring", "process-monitoring/process-monitoring-exercises.rst",
            "aeration-rate.csv", 2, "CUSUM chart of an aeration rate, which shifts after 300 minutes"),
    Example("least-squares-modelling", 4, "Least Squares Modelling Review",
            "least-squares-modelling/least-squares-model-analysis.rst", "The distances each model minimizes", 1,
            "Two least-squares lines: y from x, and x from y"),
    Example("design-analysis-experiments", 5, "Design and Analysis of Experiments",
            "design-analysis-experiments/multi-response-optimization.rst", "def surface(fit", 1,
            "Profit and purity response surfaces from a designed experiment"),
    Example("latent-variable-modelling", 6, "Latent Variable Modelling",
            "latent-variable-modelling/principal-component-analysis/pca-exercises.rst",
            "silicon-wafer-thickness.csv", 1, "PCA score plot: wafers far outside the 95% limit"),
]  # fmt: skip


def run_until(example: Example):
    """Run the example's chapter up to and including the example; return the figure it shows."""
    import plotly.basedatatypes as basedatatypes

    unit = next(u for u in ccb.build_units() if u.name == example.chapter)
    target = next(
        b
        for b in unit.blocks
        if Path(b.path).resolve() == (ROOT / example.file).resolve() and example.snippet in b.source
    )
    shown = []
    basedatatypes.BaseFigure.show = lambda fig, *args, **kwargs: shown.append(fig)
    # An example that draws unseeded random numbers (the dice) then gives the same picture each run.
    np.random.seed(2010)
    namespace = {"__name__": "__pid_book__"}
    for block in unit.blocks:
        shown.clear()
        outcome = ccb.run_block(block, namespace)
        if block is target:
            if outcome.status != "passed" or len(shown) < example.figure:
                raise RuntimeError(
                    f"{block.label}: {outcome.status}, {len(shown)} figures\n{outcome.detail}"
                )
            return shown[example.figure - 1]
    raise RuntimeError(f"never reached {example.file}")


def draw(fig, width: int, height: int, scale: float) -> np.ndarray:
    """Plotly's own rendering of ``fig`` at ``width`` x ``height`` CSS pixels, enlarged ``scale`` times."""
    # Tighter margins and no legend, so the plot fills the small tile; the data are untouched.
    fig.update_layout(
        margin={"l": 60, "r": 20, "t": 40, "b": 50}, width=None, height=None, showlegend=False
    )
    png = fig.to_image(format="png", width=width, height=height, scale=scale)
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGB"))


def canvas(width: int, height: int, background: str):
    fig = plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI, facecolor=background)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def run_pill(ax, x, y, size=1.0, z=6):
    """The book's Run in browser button, with its left edge at ``x`` and its centre at height ``y``."""
    w, h = 226 * size, 44 * size
    box(ax, x, y - h / 2, w, h, "white", LINK, radius=7 * size, lw=2 * size, z=z)
    play_icon(ax, x + 18 * size, y, 13 * size, LINK, z=z + 1)
    ax.text(x + 42 * size, y, "Run in browser", color=LINK, fontproperties=SANS, fontsize=16 * size,
            va="center_baseline", zorder=z + 1)  # fmt: skip


def save(fig, path: Path, background: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, facecolor=background)
    plt.close(fig)
    Image.open(path).convert("RGB").save(path, optimize=True)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1e3:.0f} kB)")


def banner(pictures: dict[str, np.ndarray], dark: bool) -> None:
    """Six tiles under a headline: the README's and the landing page's banner."""
    width, height = 2400, 1350
    background, ink, subink = (NAVY, NAVY_INK, NAVY_SUBINK) if dark else (BG, INK, SUBINK)
    fig, ax = canvas(width, height, background)
    ax.text(60, height - 92, "Run the book's examples in your browser", color=ink, fontproperties=SERIF, fontsize=50,
            va="center")  # fmt: skip
    ax.text(62, height - 170, "Over 180 Python examples in chapters 1 to 6, free to read and run:  learnche.org/pid",
            color=subink, fontproperties=SANS, fontsize=24, va="center")  # fmt: skip

    tile_w, tile_h, gap, top = 740, 520, 30, height - 240
    for k, example in enumerate(EXAMPLES):
        x = 60 + (k % 3) * (tile_w + gap)
        y = top - (k // 3 + 1) * tile_h - (k // 3) * gap
        box(ax, x, y, tile_w, tile_h, CARD, "none" if dark else "#DDD6C8", radius=18, z=2)
        ax.text(x + 26, y + tile_h - 40, f"{example.number}", color=ACCENT, fontproperties=SANS_BOLD, fontsize=22,
                va="center", zorder=4)  # fmt: skip
        ax.text(x + 62, y + tile_h - 40, example.title, color=INK, fontproperties=SANS_BOLD, fontsize=19,
                va="center", zorder=4)  # fmt: skip
        ax.imshow(
            pictures[example.chapter],
            extent=(x + 22, x + tile_w - 22, y + 80, y + tile_h - 72),
            zorder=3,
        )
        run_pill(ax, x + 26, y + 42, size=0.95)
    save(fig, STATIC / f"banner-{'dark' if dark else 'light'}.png", background)


def chapter_card(example: Example, picture: np.ndarray) -> None:
    """The 2:1 card a shared link to a page of this chapter shows."""
    width, height = 2560, 1280
    fig, ax = canvas(width, height, BG)
    ax.add_patch(plt.Rectangle((78, 150), 12, 980, fc=ACCENT, ec="none"))
    x = 170
    ax.text(x, 1078, f"PROCESS IMPROVEMENT USING DATA   ·   CHAPTER {example.number}", color=ACCENT,
            fontproperties=SANS_BOLD, fontsize=22, va="center")  # fmt: skip
    ax.text(x - 4, 1010, "\n".join(textwrap.wrap(example.title, 16)), color=INK, fontproperties=SERIF,
            fontsize=86, va="top", linespacing=1.02)  # fmt: skip
    ax.text(x, 470, "A free online textbook.\nRun its Python examples in your browser.", color=SUBINK,
            fontproperties=SANS, fontsize=28, va="top", linespacing=1.45)  # fmt: skip
    ax.text(x, 128, "KEVIN G. DUNN", color=INK, fontproperties=SANS_BOLD, fontsize=23, va="center")
    ax.text(
        x + 300,
        128,
        "learnche.org/pid",
        color=SUBINK,
        fontproperties=SANS,
        fontsize=23,
        va="center",
    )

    left, bottom, card_w, card_h = 1160, 120, 1330, 1040
    box(ax, left + 10, bottom - 14, card_w, card_h, "#00000014", radius=26, z=1)
    box(ax, left, bottom, card_w, card_h, CARD, "#DDD6C8", radius=26, z=2)
    ax.imshow(
        picture,
        extent=(left + 40, left + card_w - 40, bottom + 150, bottom + card_h - 40),
        zorder=3,
    )
    run_pill(ax, left + 48, bottom + 92, size=1.25)
    ax.text(left + 350, bottom + 92, example.caption, color=SUBINK, fontproperties=SANS, fontsize=19,
            va="center_baseline", zorder=4)  # fmt: skip
    save(fig, STATIC / "social" / f"{example.chapter}.png", BG)


def main() -> None:
    ccb.configure_environment()
    tiles, cards = {}, {}
    for example in EXAMPLES:
        fig = run_until(example)
        tiles[example.chapter] = draw(fig, 520, 274, scale=1.34)  # the banner's 696 x 368 tile area
        cards[example.chapter] = draw(fig, 625, 425, scale=2)  # the card's 1250 x 850 picture area
        print(f"chapter {example.number}: {example.caption}", flush=True)
    banner(tiles, dark=False)
    banner(tiles, dark=True)
    for example in EXAMPLES:
        chapter_card(example, cards[example.chapter])


if __name__ == "__main__":
    main()
