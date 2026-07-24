# Cumulative normal and t-distributions, at two degrees of freedom.
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

z = np.arange(-5, 5.001, 0.1)
normal = stats.norm.cdf(z)

fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("df = 6", "df = 35"))
for column, dof in ((1, 6), (2, 35)):
    fig.add_scatter(x=z, y=normal, mode="markers", name="Normal distribution",
                    marker={"size": 3}, row=1, col=column)
    fig.add_scatter(x=z, y=stats.t.cdf(z, df=dof), mode="lines",
                    name=f"t-distribution (df={dof})", row=1, col=column)
    fig.update_xaxes(title_text="z", row=1, col=column)
fig.update_yaxes(title_text="Cumulative probability", row=1, col=1)
fig.show()
