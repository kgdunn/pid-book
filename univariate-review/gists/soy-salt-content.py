# Salt content, mg per 15 mL serving, for 13 soy sauces.
import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation

pd.options.plotting.backend = "plotly"

salt = pd.Series([460, 520, 580, 700, 760, 770, 890, 910,
                  920, 940, 960, 1060, 1100])

print(f"mean   = {salt.mean():.1f}")          # 813.1
print(f"median = {salt.median():.0f}")        # 890
print(f"sd     = {salt.std():.1f}")           # 202.1
# scale="normal" applies the 1.4826 factor, so the MAD is comparable
# with the standard deviation for normally distributed data.
print(f"MAD    = {median_abs_deviation(salt, scale='normal'):.1f}")   # 192.7
q1, q3 = np.percentile(salt, [25, 75])
print(f"IQR    = {q3 - q1:.0f}")              # 240 = 940 - 700

fig = salt.plot.box()
fig.update_layout(yaxis_title_text="Salt content (mg / 15mL serving)",
                  showlegend=False)
fig.show()

# Testing robustness: replace one value with an artificial outlier.
salt[1] = 91941
print(f"mean   = {salt.mean():.0f}")          # 7845, not robust at all
print(f"median = {salt.median():.0f}")        # 910, robust
print(f"sd     = {salt.std():.0f}")           # 25268, way off
print(f"MAD    = {median_abs_deviation(salt, scale='normal'):.1f}")   # 222.4
