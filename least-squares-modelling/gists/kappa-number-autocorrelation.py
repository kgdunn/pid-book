# How far apart must samples be before they stop being correlated?
import numpy as np
import pandas as pd
import plotly.graph_objects as go

kappa = pd.read_csv("https://openmv.net/file/kappa-number.csv")["Kappa"].to_numpy(float)
jumps = 5
subsampled = kappa[::jumps]


def acf(series, lags=50):
    centred = series - series.mean()
    denominator = (centred ** 2).sum()
    return np.array([1.0] + [(centred[:-k] * centred[k:]).sum() / denominator
                             for k in range(1, lags + 1)])


for label, series in (("raw", kappa), (f"every {jumps}th value", subsampled)):
    values = acf(series)
    print(f"{label}: lag-1 autocorrelation {values[1]:.3f}")
    fig = go.Figure()
    fig.add_bar(x=np.arange(len(values)), y=values)
    band = 1.96 / np.sqrt(len(series))
    for sign in (1, -1):
        fig.add_hline(y=sign * band, line_dash="dash")
    fig.update_layout(xaxis_title_text="Lag",
                      yaxis_title_text="Autocorrelation",
                      title_text=f"Autocorrelation: {label}")
    fig.show()
