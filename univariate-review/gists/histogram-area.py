# Create 1000 normally distributed points
# with mean of 0 and standard deviation of 1.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

N = 1000
values = pd.Series(np.random.normal(loc=0, scale=1, size=N))

# Frequency histogram (counts).
fig = values.plot.hist()
fig.update_layout(
    yaxis_title_text=f"Frequency (N={N})",
    showlegend=False,
)
fig.show()

# Relative-density histogram (area sums to 1).
fig = values.plot.hist(histnorm="probability density")
fig.update_layout(
    yaxis_title_text="Relative density",
    showlegend=False,
)
fig.show()
