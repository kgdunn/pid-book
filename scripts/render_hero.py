"""Draw the README hero, which is also the book's social card.

Run from the repo root (the script reads the food texture data from openmv.net):

    uv run --no-project --with 'process-improve[all]' --with matplotlib \
        python scripts/render_hero.py

Writes ``_static/hero.png`` at 2560 x 1280 pixels, the 2:1 shape that GitHub,
LinkedIn and Slack show when a link to the book is shared. Upload the same file
as the repository's social preview (Settings, then General, then Social preview).

The left half names the book and what a reader gets. The right half is one of the
book's own examples as a reader sees it on the page: the code that fits a PCA model
to the food texture data, the "Run in browser" button under it, and the score plot
a click draws. The plot is computed here with the same library calls, so the card
shows the data set's real scores and its real 95% limit.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
from PIL import Image
from process_improve.multivariate import PCA, MCUVScaler
from pygments.lexers import PythonLexer
from pygments.token import Token

OUT = Path(__file__).resolve().parent.parent / "_static" / "hero.png"
W, H, DPI = 2560, 1280, 100
PT = DPI / 72  # pixels per point

# The book's cover palette: cream page, near-black ink, red accent.
BG, INK, SUBINK, ACCENT = "#F4EFE4", "#0D1B2A", "#3D4F62", "#B83A2B"
# The HTML book's own colours for code, the run button and the plotted output.
CARD, PANEL, PANEL_EDGE, LINK, CODE_INK = "#FFFFFF", "#F3F4F5", "#D0D7DE", "#176DE8", "#1F2328"
CODE_COLOURS = [  # most specific token type first
    (Token.Keyword, "#CF222E"),
    (Token.Name.Namespace, CODE_INK),
    (Token.Name, "#8250DF"),
    (Token.Literal.String, "#0550AE"),
    (Token.Literal.Number, "#0550AE"),
    (Token.Operator, "#116329"),
]
PLOT_BG, PLOT_DOT, PLOT_LIMIT = (
    "#E5ECF6",
    "#636EFA",
    "#EF553B",
)  # Plotly's defaults, as the page draws them

SERIF = FontProperties(family=["Caladea", "DejaVu Serif"], weight="bold")
SANS = FontProperties(family=["Inter", "DejaVu Sans"])
SANS_BOLD = FontProperties(family=["Inter", "DejaVu Sans"], weight="bold")
MONO = FontProperties(family=["DejaVu Sans Mono", "monospace"])

FILE = "https://openmv.net/file/food-texture.csv"
CODE = f"""\
file = "{FILE}"
food = pd.read_csv(file, index_col=0)
food_mcuv = MCUVScaler().fit_transform(food)
model = PCA(n_components=2).fit(food_mcuv)
model.score_plot(pc_horiz=1, pc_vert=2).show()"""


def fit_food_texture() -> tuple[pd.DataFrame, np.ndarray, pd.Series]:
    """Fit the book's two-component PCA model; return scores, the 95% ellipse and R^2 per component."""
    food = pd.read_csv(FILE, index_col=0)
    model = PCA(n_components=2).fit(MCUVScaler().fit_transform(food))
    limit = model.score_plot(pc_horiz=1, pc_vert=2).data[
        1
    ]  # the trace the page draws as the 95% limit
    return model.scores_, np.column_stack([limit.x, limit.y]), model.r2_per_component_


def box(ax, x, y, w, h, face, edge="none", radius=14, lw=1.5, z=2):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            fc=face,
            ec=edge,
            lw=lw,
            zorder=z,
        )
    )


def play_icon(ax, x, y, size, colour, z=6):
    """A right-pointing triangle with its left edge at ``x`` and its centre at height ``y``."""
    ax.add_patch(
        Polygon(
            [(x, y - size / 2), (x, y + size / 2), (x + 0.87 * size, y)],
            fc=colour,
            ec="none",
            zorder=z,
        )
    )


def cursor(ax, x, y, scale=1.0, z=9):
    """A mouse pointer whose tip is at (x, y)."""
    pts = (
        np.array([(0, 0), (0, -46), (11, -35), (19, -54), (27, -50), (19, -32), (34, -32)]) * scale
    )
    ax.add_patch(
        Polygon(pts + (x, y), closed=True, fc=INK, ec="white", lw=3, joinstyle="round", zorder=z)
    )


def draw_code(ax, x, top, size):
    """Syntax-colour ``CODE`` the way the HTML book does, one monospace cell per character."""
    advance, line_height = 0.6021 * size * PT, 1.62 * size * PT
    col, row = 0, 0
    for ttype, value in PythonLexer().get_tokens(CODE):
        colour = next((c for t, c in CODE_COLOURS if ttype in t), CODE_INK)
        for i, part in enumerate(value.split("\n")):
            if i:
                col, row = 0, row + 1
            if part:
                ax.text(
                    x + col * advance,
                    top - row * line_height,
                    part,
                    color=colour,
                    fontproperties=MONO,
                    fontsize=size,
                    va="top",
                    ha="left",
                    zorder=5,
                )
                col += len(part)


def draw_left(ax):
    ax.add_patch(Rectangle((78, 150), 12, 980, fc=ACCENT, ec="none"))
    x = 170
    ax.text(
        x,
        1078,
        "FREE ONLINE TEXTBOOK   ·   SINCE 2010",
        color=ACCENT,
        fontproperties=SANS_BOLD,
        fontsize=22,
        va="center",
    )
    ax.text(
        x - 4,
        1012,
        "Process\nImprovement\nusing Data",
        color=INK,
        fontproperties=SERIF,
        fontsize=90,
        va="top",
        linespacing=1.0,
    )
    ax.text(
        x,
        560,
        "Statistics and chemometrics for engineers and\nscientists who work with process data.",
        color=SUBINK,
        fontproperties=SANS,
        fontsize=27,
        va="top",
        linespacing=1.45,
    )
    ax.plot([x, 1080], [418, 418], color="#C9C0AE", lw=1.5)

    rows = [
        ("run", "Python examples that run in your browser"),
        ("dot", "Real data sets, exercises and worked solutions"),
        ("dot", "Free to read, download and adapt (CC BY-SA)"),
    ]
    for i, (kind, text) in enumerate(rows):
        y = 352 - i * 66
        if kind == "run":
            box(ax, x, y - 19, 52, 38, "white", LINK, radius=7, lw=2.2, z=5)
            play_icon(ax, x + 19, y, 17, LINK)
        else:
            ax.add_patch(Rectangle((x + 19, y - 7), 14, 14, fc=ACCENT, ec="none", zorder=5))
        ax.text(x + 76, y, text, color=INK, fontproperties=SANS, fontsize=25, va="center_baseline")

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


def draw_card(fig, ax, scores, ellipse, r2):
    left, bottom, width, height = 1200, 96, 1290, 1088
    box(ax, left + 10, bottom - 14, width, height, "#00000014", radius=26, z=1)  # soft shadow
    box(ax, left, bottom, width, height, CARD, "#DDD6C8", radius=26, lw=1.5, z=2)

    pad = 52
    ax.text(
        left + pad,
        bottom + height - 58,
        "6.  LATENT VARIABLE MODELLING",
        color="#57606A",
        fontproperties=SANS_BOLD,
        fontsize=17,
        va="center",
    )

    # The code block, as the page shows it.
    code_top, code_h = bottom + height - 104, 352
    box(
        ax,
        left + pad,
        code_top - code_h,
        width - 2 * pad,
        code_h,
        PANEL,
        PANEL_EDGE,
        radius=12,
        z=3,
    )
    draw_code(ax, left + pad + 34, code_top - 36, size=25.5)

    # The run button under it, with the pointer about to click.
    btn_y, btn_h, btn_w = code_top - code_h - 30 - 66, 66, 404
    box(ax, left + pad, btn_y, btn_w, btn_h, "white", LINK, radius=9, lw=2.6, z=4)
    play_icon(ax, left + pad + 30, btn_y + btn_h / 2, 20, LINK)
    ax.text(
        left + pad + 66,
        btn_y + btn_h / 2,
        "Run in browser",
        color=LINK,
        fontproperties=SANS,
        fontsize=25,
        va="center_baseline",
        zorder=6,
    )
    cursor(ax, left + pad + btn_w - 44, btn_y + btn_h / 2 + 4, scale=1.15)

    # The output panel the click opens, holding the score plot.
    out_top = btn_y - 30
    out_bottom = bottom + 44
    box(ax, left + pad, out_bottom, width - 2 * pad, out_top - out_bottom, PANEL, radius=0, z=3)
    ax.add_patch(
        Rectangle((left + pad, out_bottom), 7, out_top - out_bottom, fc=LINK, ec="none", zorder=4)
    )

    px0, py0 = left + pad + 150, out_bottom + 92
    pw, ph = width - 2 * pad - 230, out_top - out_bottom - 128
    plot = fig.add_axes([px0 / W, py0 / H, pw / W, ph / H], zorder=10)
    plot.set_facecolor(PLOT_BG)
    plot.grid(color="white", lw=2.2)
    plot.set_axisbelow(True)
    for spine in plot.spines.values():
        spine.set_visible(False)
    plot.tick_params(length=0, labelsize=17, labelcolor="#2A3F5F", pad=8)
    plot.plot(ellipse[:, 0], ellipse[:, 1], color=PLOT_LIMIT, lw=3, zorder=3)
    t = scores.to_numpy()
    plot.scatter(t[:, 0], t[:, 1], s=120, color=PLOT_DOT, edgecolor="white", lw=1.2, zorder=4)
    plot.set_xlim(np.array([-1.08, 1.08]) * np.abs(ellipse[:, 0]).max())
    plot.set_ylim(np.array([-1.12, 1.12]) * np.abs(ellipse[:, 1]).max())
    plot.set_xlabel(
        f"t1 [{r2.iloc[0]:.0%}]", fontproperties=SANS, fontsize=19, color="#2A3F5F", labelpad=8
    )
    plot.set_ylabel(
        f"t2 [{r2.iloc[1]:.0%}]", fontproperties=SANS, fontsize=19, color="#2A3F5F", labelpad=8
    )

    # A hover label on the most unusual pastry, the way the interactive plot shows one,
    # placed where it covers no other point.
    i = int(np.argmax((t**2 / t.var(axis=0)).sum(axis=1)))
    spot = clear_spot(t, i, plot.get_xlim(), plot.get_ylim(), (pw, ph))
    plot.annotate(
        scores.index[i],
        tuple(t[i]),
        xytext=spot,
        textcoords="data",
        ha="center",
        va="center",
        fontproperties=SANS_BOLD,
        fontsize=17,
        color="white",
        zorder=6,
        bbox={"boxstyle": "round,pad=0.35", "fc": PLOT_DOT, "ec": "white", "lw": 1.5},
        arrowprops={"arrowstyle": "-", "color": PLOT_DOT, "lw": 2, "shrinkA": 0, "shrinkB": 6},
    )


def clear_spot(points, i, xlim, ylim, size_px, reach_px=75, margin_px=45):
    """Return, in data units, the spot about ``reach_px`` from point ``i`` farthest from every other point.

    Distances are measured in pixels of the drawn axes (``size_px``), so a label on a wide, short
    plot is kept clear in the direction that matters. Spots closer than ``margin_px`` to an edge
    of the axes are not used.
    """
    lo = np.array([xlim[0], ylim[0]])
    px_per_unit = np.array(size_px) / np.array([xlim[1] - xlim[0], ylim[1] - ylim[0]])
    pixels = (points - lo) * px_per_unit
    others = np.delete(pixels, i, axis=0)
    best, best_gap = None, -1.0
    for angle in np.linspace(0, 2 * np.pi, 24, endpoint=False):
        spot = pixels[i] + reach_px * np.array([np.cos(angle), np.sin(angle)])
        if np.any(spot < margin_px) or np.any(spot > np.array(size_px) - margin_px):
            continue
        gap = np.min(np.linalg.norm(others - spot, axis=1))
        if gap > best_gap:
            best, best_gap = spot, gap
    return tuple(best / px_per_unit + lo)


def main() -> None:
    scores, ellipse, r2 = fit_food_texture()
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    draw_left(ax)
    draw_card(fig, ax, scores, ellipse, r2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI, facecolor=BG)
    Image.open(OUT).convert("RGB").save(
        OUT, optimize=True
    )  # no alpha channel: smaller, and every site accepts it
    print(f"wrote {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}")


if __name__ == "__main__":
    main()
