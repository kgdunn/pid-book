"""Generate the README hero / social card.

Run from the repo root:

    python scripts/render_hero.py

Writes ``_static/hero.png`` at 2560 x 1280 pixels: a six-panel preview of
the topics the book covers, with a title block on the left. This is the
image GitHub, Slack, etc. unfurl when the README is linked.

The six panels are: data visualization (box plots), distributions
(histogram with normal curve), process monitoring (control chart),
regression (scatter with fit), designed experiments (response-surface
contour), and latent variables (PCA score plot).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

# Visual constants ------------------------------------------------------------

BG = "#F4EFE4"          # cream background
INK = "#0D1B2A"         # near-black for title
SUBINK = "#3D4F62"      # softer slate for body text
ACCENT = "#B83A2B"      # red accent (vertical bar, outliers, "since 2010")
PLOT_BLUE = "#36657F"   # primary plot color
PLOT_FILL = "#A6BFCC"   # lighter shade for fills
PANEL_EDGE = "#1F2F3F"

W_IN, H_IN, DPI = 25.6, 12.8, 100  # -> 2560 x 1280 px

RNG = np.random.default_rng(20260520)

BLUES = LinearSegmentedColormap.from_list(
    "card_blues",
    ["#D6E0E7", "#A6BFCC", "#7BA3B6", "#5C8A9F", PLOT_BLUE,
     "#23607C", "#184E66", "#0F3A4F"],
)


def _label(ax, text):
    ax.set_title(text, fontsize=18, color=INK, style="italic",
                 family="serif", pad=10)


def _frame(ax):
    for spine in ax.spines.values():
        spine.set_color(PANEL_EDGE)
        spine.set_linewidth(1.0)
    ax.tick_params(left=False, bottom=False,
                   labelleft=False, labelbottom=False)


def panel_box(ax):
    _label(ax, "Data visualization")
    data = [RNG.normal(loc, 1.0, 60) for loc in (0.0, 0.6, 0.3, 1.0, 0.4)]
    bp = ax.boxplot(
        data, patch_artist=True, widths=0.55,
        medianprops=dict(color="white", linewidth=1.6),
        flierprops=dict(marker="o", markerfacecolor=ACCENT,
                        markeredgecolor=ACCENT, markersize=4),
    )
    for box in bp["boxes"]:
        box.set(facecolor=PLOT_BLUE, edgecolor=PANEL_EDGE, linewidth=0.8)
    for line in bp["whiskers"] + bp["caps"]:
        line.set(color=PANEL_EDGE, linewidth=0.8)
    _frame(ax)


def panel_hist(ax):
    _label(ax, "Distributions")
    sample = RNG.normal(0, 1, 4000)
    counts, edges, _ = ax.hist(
        sample, bins=36, color=PLOT_FILL,
        edgecolor=PANEL_EDGE, linewidth=0.4,
    )
    xs = np.linspace(-4, 4, 200)
    pdf = (1 / np.sqrt(2 * np.pi)) * np.exp(-xs ** 2 / 2)
    ax.plot(xs, pdf * counts.max() / pdf.max(),
            color=ACCENT, linewidth=2.2)
    _frame(ax)


def panel_monitor(ax):
    _label(ax, "Process monitoring")
    n = 70
    y = RNG.normal(0, 1, n)
    y[37] = 4.2
    ax.axhspan(-3, 3, color=PLOT_FILL, alpha=0.30)
    ax.axhline(0, color=PANEL_EDGE, linewidth=0.6)
    ax.axhline(3, color=ACCENT, linestyle="--", linewidth=1.1)
    ax.axhline(-3, color=ACCENT, linestyle="--", linewidth=1.1)
    ax.plot(np.arange(n), y, color=PLOT_BLUE,
            linewidth=1.0, marker=".", markersize=4)
    ax.plot(37, y[37], "o", color=ACCENT, markersize=9)
    ax.set_ylim(-4.5, 5)
    _frame(ax)


def panel_regression(ax):
    _label(ax, "Regression")
    x = np.linspace(0, 10, 40)
    y = 0.8 * x + RNG.normal(0, 0.7, len(x))
    ax.scatter(x, y, s=14, color=PLOT_BLUE,
               edgecolors=PANEL_EDGE, linewidths=0.3)
    xs = np.linspace(0, 10, 100)
    ax.plot(xs, 0.8 * xs, color=PLOT_BLUE, linewidth=1.8)
    ax.fill_between(xs, 0.8 * xs - 1.0, 0.8 * xs + 1.0,
                    color=PLOT_FILL, alpha=0.40)
    high_lev = np.array([[0.4, -1.7], [1.2, -0.9]])
    ax.scatter(high_lev[:, 0], high_lev[:, 1], s=70, color=ACCENT,
               edgecolors="white", linewidths=1.0, zorder=5)
    ax.set_ylim(-2.4, 9.5)
    _frame(ax)


def panel_doe(ax):
    _label(ax, "Designed experiments")
    g = np.linspace(-1.5, 1.5, 200)
    X, Y = np.meshgrid(g, g)
    Z = -(X ** 2 + Y ** 2)
    ax.contourf(X, Y, Z, levels=8, cmap=BLUES)
    pts = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0),
           (1.3, 0), (-1.3, 0), (0, 1.3), (0, -1.3)]
    px, py = zip(*pts)
    ax.scatter(px, py, s=55, facecolor=ACCENT, edgecolors="white",
               linewidths=1.0, zorder=5)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    _frame(ax)


def panel_lvm(ax):
    _label(ax, "Latent variables")
    n = 150
    raw = RNG.normal(0, 1, size=(n, 2)) * np.array([1.4, 0.9])
    angle = 0.4
    rot = np.array([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle),  np.cos(angle)]])
    pts = raw @ rot.T
    ax.scatter(pts[:, 0], pts[:, 1], s=14, color=PLOT_BLUE,
               edgecolors=PANEL_EDGE, linewidths=0.2)
    theta = np.linspace(0, 2 * np.pi, 200)
    ell = np.column_stack([3.0 * np.cos(theta), 1.9 * np.sin(theta)]) @ rot.T
    ax.plot(ell[:, 0], ell[:, 1], color=PLOT_BLUE,
            linewidth=0.8, linestyle=(0, (4, 3)))
    outs = np.array([[3.4, 1.8], [-3.6, 0.8], [0.5, -2.4]])
    ax.scatter(outs[:, 0], outs[:, 1], s=70, color=ACCENT, marker="x",
               linewidths=2.0)
    ax.axhline(0, color=PANEL_EDGE, linewidth=0.4)
    ax.axvline(0, color=PANEL_EDGE, linewidth=0.4)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-3.5, 3.5)
    _frame(ax)


def main():
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=BG)

    outer = GridSpec(1, 2, width_ratios=[0.42, 0.58],
                     left=0.02, right=0.985, top=0.94, bottom=0.06,
                     wspace=0.05)

    ax_title = fig.add_subplot(outer[0, 0])
    ax_title.set_axis_off()

    fig.patches.append(
        mpatches.Rectangle(
            (0.030, 0.10), 0.0035, 0.78,
            transform=fig.transFigure, color=ACCENT,
            zorder=10, clip_on=False,
        )
    )

    TEXT_X = 0.17

    ax_title.text(TEXT_X, 0.88,
                  "AN OPEN TEXTBOOK   ·   SINCE 2010",
                  fontsize=20, color=ACCENT, fontweight="bold",
                  family="sans-serif", transform=ax_title.transAxes)

    ax_title.text(TEXT_X, 0.62, "Process\nImprovement\nusing Data",
                  fontsize=64, color=INK, family="serif",
                  fontweight="bold", linespacing=1.10,
                  transform=ax_title.transAxes,
                  verticalalignment="center")

    ax_title.plot([TEXT_X, 0.86], [0.32, 0.32],
                  color=SUBINK, linewidth=0.8,
                  transform=ax_title.transAxes, clip_on=False)

    ax_title.text(TEXT_X, 0.23,
                  "Statistics & chemometrics for engineers\n"
                  "and scientists who work with process data.",
                  fontsize=20, color=SUBINK, family="sans-serif",
                  linespacing=1.35,
                  transform=ax_title.transAxes)

    ax_title.text(TEXT_X, 0.11, "KEVIN G. DUNN",
                  fontsize=22, color=INK, fontweight="bold",
                  family="sans-serif", transform=ax_title.transAxes)

    ax_title.text(TEXT_X, 0.04,
                  "Free   ·   CC BY-SA   ·   learnche.org/pid",
                  fontsize=15, color=SUBINK, family="sans-serif",
                  transform=ax_title.transAxes)

    inner = GridSpec(2, 3,
                     left=0.46, right=0.985, top=0.88, bottom=0.10,
                     wspace=0.18, hspace=0.40)

    panel_box(fig.add_subplot(inner[0, 0]))
    panel_hist(fig.add_subplot(inner[0, 1]))
    panel_monitor(fig.add_subplot(inner[0, 2]))
    panel_regression(fig.add_subplot(inner[1, 0]))
    panel_doe(fig.add_subplot(inner[1, 1]))
    panel_lvm(fig.add_subplot(inner[1, 2]))

    out = Path(__file__).resolve().parent.parent / "_static" / "hero.png"
    fig.savefig(out, dpi=DPI, facecolor=BG)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
