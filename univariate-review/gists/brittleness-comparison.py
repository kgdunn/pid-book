# Compare the brittleness index from three reactors, pairwise.
import numpy as np
import pandas as pd
from scipy import stats

pd.options.plotting.backend = "plotly"

brittle = pd.read_csv("https://openmv.net/file/brittleness-index.csv")

fig = brittle.plot.box()
fig.update_layout(yaxis_title_text="Brittleness index", showlegend=False)
fig.show()


def group_difference(group_a, group_b):
    """z-value and 95% interval for the difference in two means.

    The groups have different numbers of measurements, and missing
    values, so each one is cleaned separately.
    """
    a = group_a.dropna().to_numpy()
    b = group_b.dropna().to_numpy()
    dof = len(a) - 1 + len(b) - 1
    pooled = ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / dof
    spread = np.sqrt(pooled * (1 / len(a) + 1 / len(b)))
    difference = b.mean() - a.mean()
    critical = stats.t.ppf(0.975, df=dof)
    return (difference / spread,
            difference - critical * spread,
            difference + critical * spread)


for first, second in (("TK104", "TK105"), ("TK104", "TK107"),
                      ("TK105", "TK107")):
    z, lower, upper = group_difference(brittle[first], brittle[second])
    print(f"{first} vs {second}: z = {z:.3f}, {lower:.1f} < diff < {upper:.1f}")
# TK104 vs TK105: z =  1.254
# TK104 vs TK107: z =  1.406
# TK105 vs TK107: z = -0.053
