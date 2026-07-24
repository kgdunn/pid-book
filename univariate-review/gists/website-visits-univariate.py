# Do the daily website visits follow a normal distribution?
import numpy as np
import pandas as pd
from scipy import stats

pd.options.plotting.backend = "plotly"

web = pd.read_csv("https://openmv.net/file/website-traffic.csv")
visits = web["Visits"]

fig = visits.plot.hist()
fig.update_layout(xaxis_title_text="Number of visits", showlegend=False)
fig.show()

# A q-q plot: sorted data against the matching normal quantiles.
ordered = np.sort(visits)
quantiles = stats.norm.ppf((np.arange(1, len(ordered) + 1) - 0.375)
                           / (len(ordered) + 0.25))
fig = pd.DataFrame({"Normal quantiles": quantiles,
                    "Visits": ordered}).plot.scatter(x="Normal quantiles",
                                                    y="Visits")
fig.show()

mean, sd = visits.mean(), visits.std()
print(f"mean = {mean:.2f}, sd = {sd:.2f}")            # 22.23 and 8.33
inside = stats.norm.cdf((30 - mean) / sd) - stats.norm.cdf((10 - mean) / sd)
print(f"P(10 < visits < 30) = {inside:.3f}")          # 0.753
