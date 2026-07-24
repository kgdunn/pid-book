# Properties of a powder: plot each variable in sequence order and
# look for unusual points.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

raw = pd.read_csv("https://openmv.net/file/raw-material-properties.csv")
print(raw.shape)     # (36, 7): 36 observations of 7 columns

labels = {
    "size1": "Particle size: level 1",
    "size2": "Particle size: level 2",
    "size3": "Particle size: level 3",
    "density1": "Particle density: level 1",
    "density2": "Particle density: level 2",
    "density3": "Particle density: level 3",
}
for column, label in labels.items():
    fig = raw[column].plot.line(markers=True, text=raw["Sample"])
    fig.update_traces(mode="markers", hovertemplate="%{text}: %{y}")
    fig.update_layout(xaxis_title_text="Index",
                      yaxis_title_text=label,
                      showlegend=False)
    fig.show()

    # Which samples fall outside the 1.5 IQR fences?
    q1, q3 = np.percentile(raw[column].dropna(), [25, 75])
    iqr = q3 - q1
    beyond = (raw[column] < q1 - 1.5 * iqr) | (raw[column] > q3 + 1.5 * iqr)
    print(column, list(raw.loc[beyond, "Sample"]))
