# The supplier reported only the histogram, not the 50 raw values.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

centres = np.array([4025, 4075, 4125, 4175, 4225, 4275, 4325, 4375])
counts = np.array([4, 19, 14, 5, 4, 1, 2, 1])
N = 50

# Treat every bulb in a bin as sitting at that bin's centre.
mean = (centres * counts).sum() / N
sd = np.sqrt((counts * (centres - mean) ** 2).sum() / (N - 1))
print(f"mean = {mean:.0f}, sd = {sd:.1f}")            # 4127 and 78.9

fig = pd.Series(counts, index=centres).plot.bar()
fig.update_layout(xaxis_title_text="Energy required over 24 hours (W.h)",
                  yaxis_title_text=f"Number of bulbs (N={N})",
                  showlegend=False)
fig.show()
