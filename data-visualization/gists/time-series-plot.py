import pandas as pd
import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"

# Real ammonia concentrations from a waste-water treatment plant.
waste = pd.read_csv("https://openmv.net/file/ammonia.csv")

# Give the x-axis real time units rather than raw integer indices.
# The CSV ships without a timestamp; attach an hourly index that
# starts at the beginning of 2010 so the time axis is meaningful.
waste.index = pd.date_range(
    start="2010-01-01", periods=len(waste), freq="h"
)

# A clean line plot of the raw signal, with month/year tick labels.
fig = waste["Ammonia"].plot.line()
fig.update_layout(
    xaxis_title_text="Date",
    yaxis_title_text="Ammonia [mmol/L]",
    width=800,
    height=400,
    showlegend=False,
)
fig.update_xaxes(tickformat="%b %Y")
fig.show()

# Overlay a 5-day rolling mean to separate signal from noise.
rolling = waste["Ammonia"].rolling("5D", center=True).mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=waste.index, y=waste["Ammonia"], name="Ammonia"))
fig.add_trace(
    go.Scatter(
        x=waste.index,
        y=rolling,
        name="5-day rolling mean",
        line_color="black",
    )
)
fig.update_layout(
    xaxis_title_text="Date",
    yaxis_title_text="Ammonia [mmol/L]",
    width=800,
    height=400,
)
fig.update_xaxes(tickformat="%b %Y")
fig.show()
