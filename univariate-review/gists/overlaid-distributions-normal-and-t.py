# The normal and t densities for a sample of 7, so 6 degrees of freedom.
import numpy as np
import plotly.graph_objects as go
from scipy import stats

n = 7
z = np.arange(-5, 5.001, 0.01)

fig = go.Figure()
fig.add_scatter(x=z, y=stats.norm.pdf(z), mode="lines",
                name="Normal distribution")
fig.add_scatter(x=z, y=stats.t.pdf(z, df=n - 1), mode="lines",
                line_dash="dash", name=f"t-distribution (df={n - 1})")
fig.update_layout(xaxis_title_text="z",
                  yaxis_title_text="Normal and t-distributions")
fig.show()
