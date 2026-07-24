# Least squares by hand, and with a library, on the distillation data.
import numpy as np
import pandas as pd
from scipy import stats

pd.options.plotting.backend = "plotly"

tower = pd.read_csv("https://openmv.net/file/distillation-tower.csv")
x = tower["TempC2"].to_numpy(float)
y = tower["VapourPressure"].to_numpy(float)
n = len(x)

# Model coefficients, straight from the definitions.
x_bar, y_bar = x.mean(), y.mean()
numerator = ((x - x_bar) * (y - y_bar)).sum()
denominator = ((x - x_bar) ** 2).sum()
b1 = numerator / denominator
b0 = y_bar - b1 * x_bar
print(f"VapourPressure = {b0:.1f} {b1:+.4f} TempC2")

predictions = b0 + b1 * x
residuals = y - predictions

# The three standard errors.
SE = np.sqrt((residuals ** 2).sum() / (n - 2))
SE_b1 = np.sqrt(SE ** 2 / denominator)
SE_b0 = np.sqrt(SE ** 2 * (1 / n + x_bar ** 2 / denominator))
print(f"S_E = {SE:.3f}, SE(b0) = {SE_b0:.2f}, SE(b1) = {SE_b1:.5f}")

# 99% confidence intervals for the two coefficients.
critical = stats.t.ppf(0.995, df=n - 2)
print(f"b0 in {b0 - critical * SE_b0:.1f} to {b0 + critical * SE_b0:.1f}")
print(f"b1 in {b1 - critical * SE_b1:.4f} to {b1 + critical * SE_b1:.4f}")

# R2 and the sums of squares.
TSS = ((y - y_bar) ** 2).sum()
RSS = (residuals ** 2).sum()
print(f"TSS = {TSS:.0f}, RSS = {RSS:.0f}, R2 = {1 - RSS / TSS:.3f}")

fig = tower.plot.scatter(x="TempC2", y="VapourPressure")
fig.add_scatter(x=x, y=predictions, mode="lines", name="Least squares fit")
fig.update_layout(xaxis_title_text="Tray temperature [°F]",
                  yaxis_title_text="Vapour pressure [kPa]")
fig.show()
