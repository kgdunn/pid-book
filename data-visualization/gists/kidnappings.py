# Approximate values read off the time-series plot, 1996 to 2007.
import pandas as pd

pd.options.plotting.backend = "plotly"

colombia = pd.DataFrame({
    "Year": range(1996, 2008),
    "Kidnap": [4, 5, 6.5, 7.5, 8.75, 7, 7, 5, 3.25, 2, 1.5, 1.25],
    "Mobile": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 2, 3.5, 4.25, 6.5, 7.25],
})

fig = colombia.plot.scatter(x="Mobile", y="Kidnap", text="Year")
fig.update_traces(mode="markers")
fig.update_layout(
    xaxis_title_text="Mobile phone antennae [thousands]",
    yaxis_title_text="Kidnappings per 100,000 residents",
)
fig.show()
