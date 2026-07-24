# Prediction intervals at three new temperatures.
import numpy as np
import pandas as pd
from scipy import stats

pd.options.plotting.backend = "plotly"

tower = pd.read_csv("https://openmv.net/file/distillation-tower.csv")
x = tower["TempC2"].to_numpy(float)
y = tower["VapourPressure"].to_numpy(float)
n = len(x)

b1, b0 = np.polyfit(x, y, 1)
residuals = y - (b0 + b1 * x)
SE = np.sqrt((residuals ** 2).sum() / (n - 2))
Sxx = ((x - x.mean()) ** 2).sum()
critical = stats.t.ppf(0.975, df=n - 2)

new = np.array([430.0, 480.0, 520.0])
fit = b0 + b1 * new
# The extra 1 inside the square root is what makes this a prediction
# interval for a new observation, not a confidence interval for the line.
spread = SE * np.sqrt(1 + 1 / n + (new - x.mean()) ** 2 / Sxx)
for t, f, s in zip(new, fit, spread):
    print(f"T = {t:.0f}: {f:.2f}, 95% PI {f - critical * s:.2f} to {f + critical * s:.2f}")

fig = tower.plot.scatter(x="TempC2", y="VapourPressure")
fig.add_scatter(x=x, y=b0 + b1 * x, mode="lines", name="Least squares fit")
fig.add_scatter(x=new, y=fit, mode="markers", name="Prediction intervals",
                error_y={"type": "data", "array": critical * spread})
fig.update_layout(xaxis_title_text="Tray temperature [°F]",
                  yaxis_title_text="Vapour pressure [kPa]")
fig.show()
