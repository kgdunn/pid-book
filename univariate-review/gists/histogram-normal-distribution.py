# Create 500 normally distributed points
# with a mean of 1100 and standard deviation
# of 50 units.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

N = 500
values = pd.Series(np.random.normal(loc=1100, scale=50, size=N))

fig = values.plot.hist(nbins=8)
fig.update_layout(
    xaxis_title_text="Mass [g] of each package",
    yaxis_title_text=f"Number of packages (N={N})",
    showlegend=False,
)
fig.show()
