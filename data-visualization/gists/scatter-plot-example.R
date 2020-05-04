# Plot of temperature vs vapour pressure
data_file = "https://openmv.net/file/distillation-tower.csv"
distillation = read.csv(data_file)

plot(distillation$Temp9,
     distillation$VapourPressure,
     xlab="Temperature (F)",
     ylab="Vapour pressure (kPa)")

# Plot of white hairs vs BMD
#    Osteoporosis (fake) data: number of white
#    hairs per square inch vs bone mineral
#    density (measurement of osteoporosis)
#    vs kg/m^3 (1500 kg/m3 is typical)
N = 50
white.hairs = round(rnorm(N,
                    mean=500,
                    sd=150))
bone.mineral.density = -0.25 * white.hairs + 1550 + rnorm(N, mean=0, sd=25)

plot(white.hairs, bone.mineral.density,
     xlab = "Number of white hairs per square inch of scalp",
     ylab = "Bone mineral density (kg/m^3) [measure of osteoporosis]")