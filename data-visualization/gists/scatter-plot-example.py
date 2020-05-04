import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Plot of temperature vs vapour pressure
data_file = "https://openmv.net/file/distillation-tower.csv"
distillation = pd.read_csv(data_file)
ax = distillation.plot.scatter(x="Temp9", y="VapourPressure")
ax.set_xlabel("Temperature (F)")
ax.set_ylabel("Vapour pressure (kPa)")
plt.show()

# Plot of white hairs vs BMD
#    Osteoporosis (fake) data: number of white
#    hairs per square inch vs bone mineral
#    density (measurement of osteoporosis)
#    vs kg/m^3 (1500 kg/m3 is typical)
N = 50
white_hairs = np.random.normal(loc=500, scale=150, size=N)
bone_mineral_density = -0.25 * white_hairs + 1550 + np.random.normal(loc=0, scale=25, size=N)
fig2, ax2 = plt.subplots(nrows=1, ncols=1)
ax2.plot(white_hairs, bone_mineral_density, "o", ms=10)
ax2.set_xlabel("Number of white hairs per square inch of scalp")
ax2.set_ylabel("Bone mineral density (kg/m$^3$) [measure of osteoporosis]")
plt.show()
