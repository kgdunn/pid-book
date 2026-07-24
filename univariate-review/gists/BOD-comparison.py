# Two ways of measuring biochemical oxygen demand, on eleven samples
# that were each split in half.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

bod = pd.DataFrame({
    "Dilution": [11, 26, 18, 16, 20, 12, 8, 26, 12, 17, 14],
    "Manometric": [25, 3, 27, 30, 33, 16, 28, 27, 12, 32, 16],
})
print(bod.mean().round(1).to_dict())     # 16.4 and 22.6

# Plot the differences before calculating anything.
bod["Difference"] = bod["Dilution"] - bod["Manometric"]
bod["Sample"] = range(1, len(bod) + 1)
fig = bod.plot.scatter(x="Sample", y="Difference")
fig.add_hline(y=0)
fig.update_layout(xaxis_title_text="Sample number",
                  yaxis_title_text="Dilution - Manometric",
                  showlegend=False)
fig.show()
