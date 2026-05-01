import numpy as np
import pandas as pd

pd.options.plotting.backend = "plotly"

# Plot of temperature vs vapour pressure.
data_file = "http://openmv.net/file/distillation-tower.csv"
distillation = pd.read_csv(data_file)
fig = distillation.plot.scatter(x="Temp9", y="VapourPressure")
fig.update_layout(
    xaxis_title_text="Temperature (F)",
    yaxis_title_text="Vapour pressure (kPa)",
)
fig.show()

# Plot of white hairs vs BMD.
#   Osteoporosis (fake) data: number of white
#   hairs per square inch vs bone mineral
#   density (measurement of osteoporosis)
#   in kg/m^3 (1500 kg/m3 is typical).
N = 50
white_hairs = np.round(np.random.normal(loc=500, scale=150, size=N))
bone_mineral_density = (
    -0.25 * white_hairs + 1550 + np.random.normal(loc=0, scale=25, size=N)
)
osteo = pd.DataFrame(
    {"white_hairs": white_hairs, "bone_mineral_density": bone_mineral_density}
)
fig = osteo.plot.scatter(x="white_hairs", y="bone_mineral_density")
fig.update_layout(
    xaxis_title_text="Number of white hairs per square inch of scalp",
    yaxis_title_text="Bone mineral density (kg/m^3) [measure of osteoporosis]",
)
fig.show()
