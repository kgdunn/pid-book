# Correlation among the cheese predictors, and what it does to a model.
import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

cheese = pd.read_csv("https://openmv.net/file/cheddar-cheese.csv")
print(cheese[["Acetic", "H2S", "Lactic", "Taste"]].corr().round(2))

fig = cheese.plot.scatter(x="Acetic", y="Taste")
fig.show()

# Mean-centering changes the intercept, not the slope.
x, y = cheese["Acetic"].to_numpy(float), cheese["Taste"].to_numpy(float)
print(np.polyfit(x, y, 1))
print(np.polyfit(x - x.mean(), y - y.mean(), 1))

# All three predictors together.
X = np.column_stack([np.ones(len(cheese)), cheese["Acetic"],
                     cheese["H2S"], cheese["Lactic"]])
coefficients, *_ = np.linalg.lstsq(X, y, rcond=None)
print("Taste =", " + ".join(f"{c:.2f}" for c in coefficients))
