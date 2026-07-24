# The four cases from the recipe above, each with a different
# resolution on the measurement axis.
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

rng = np.random.default_rng(19)

# A: acceptable or unacceptable metal appearance, coded 1 or 0.
appearance = rng.random(400) < 0.86

# B: number of defects on a metal sheet, graded 1 to 4.
grade = rng.choice([1, 2, 3, 4], size=400, p=[0.46, 0.30, 0.17, 0.07])

# C: batch yield, reported to the nearest whole percent.
yields = np.round(rng.normal(loc=80, scale=4.5, size=300)).astype(int)

# D: ambient temperature, measured to 0.05 K but binned every 5 K.
temperature = rng.normal(loc=284, scale=9, size=365)

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "A: metal appearance, yes or no",
        "B: defects on a metal sheet, four grades",
        "C: batch yield, rounded to 1%",
        "D: daily temperature, binned every 5 K",
    ),
)
fig.add_bar(
    x=["Unacceptable (0)", "Acceptable (1)"],
    y=[int((~appearance).sum()), int(appearance.sum())],
    row=1,
    col=1,
)
fig.add_bar(
    x=["1: none", "2: low", "3: medium", "4: high"],
    y=np.bincount(grade, minlength=5)[1:],
    row=1,
    col=2,
)
fig.add_histogram(x=yields, xbins={"size": 1}, row=2, col=1)
fig.add_histogram(x=temperature, xbins={"start": 255, "end": 315, "size": 5},
                  row=2, col=2)

fig.update_yaxes(title_text="Number of pieces", row=1, col=1)
fig.update_yaxes(title_text="Number of sheets", row=1, col=2)
fig.update_yaxes(title_text="Number of batches", row=2, col=1)
fig.update_yaxes(title_text="Number of days", row=2, col=2)
fig.update_xaxes(title_text="Yield [%]", row=2, col=1)
fig.update_xaxes(title_text="Ambient temperature [K]", row=2, col=2)
fig.update_layout(showlegend=False, height=800)
fig.show()
