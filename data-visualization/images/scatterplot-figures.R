# Distillation data
distillation <- read.csv('/Users/kevindunn/ConnectMV/Datasets/Distillation/distillation-vapour-pressure.csv')

# Osteoporosis (fake) data: number of white hairs per square inch vs bone mineral density (measurement of osteoporosis) if kg/m^3 (1500 kg/m3 is typical)
N = 50
white.hairs = round(rnorm(N, mean=500, sd=250))
bone.mineral.density = -0.25 * white.hairs + 1550 + rnorm(N, mean=0, sd=25)

bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/scatterplot-figures.png', type="png256", res=300, pointsize=14, width=12, height=6)

m <- matrix(1:2, 1, 2)  # Plot layout
layout(m)

# Plot of temperature vs vapour pressure
plot(distillation$Temperature, distillation$Vapour.pressure, xlab="Temperature (F)", ylab="Vapour pressure (kPa)")

# Plot of white hairs vs BMD
plot(white.hairs, bone.mineral.density, xlab = "Number of white hairs per square inch of scalp", ylab = "Bone mineral density (kg/m^3) [measure of osteoporosis]")

dev.off()


# The second time through, use the car library, and change the `plot` commands to `scatterplot`
# Capture the plots from TextMate's HTML output and take a screenshot.  The "scatterplot" command seems to do strange things with the "layout" command, so we can't write to file directly.
library(car)

#bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/scatterplot-figures-with-regression-lines.png', type="png256", res=300, pointsize=14, width=12, height=6)

m <- matrix(1:2, 1, 2)  # Plot layout
layout(m)

# Plot of temperature vs vapour pressure
scatterplot(distillation$Temperature, distillation$Vapour.pressure, xlab="Temperature (F)", ylab="Vapour pressure (kPa)", col=c("black", "black", "black", "black", "black"), cex.axis=1.5, cex.lab=1.5)

# Plot of white hairs vs BMD
scatterplot(white.hairs, bone.mineral.density, xlab = "Number of white hairs per square inch of scalp", ylab = "Bone mineral density (kg/m^3) [measure of osteoporosis]", col=c("black", "black", "black", "black", "black"), cex.axis=1.5, cex.lab=1.5)

#dev.off()


# These plots are for the slides:


bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/scatterplot-temperature-vs-vapour-pressure.png', type="png256", res=300, pointsize=14, width=6, height=6)
# bottom, left, top, right: spacing
par(mar=c(5, 4, 0, 0) + 0.1)
plot(distillation$Temperature, distillation$Vapour.pressure, xlab="Temperature (F)", ylab="Vapour pressure (kPa)")
dev.off()


bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/scatterplot-white-hairs-vs-BMD.png', type="png256", res=300, pointsize=14, width=6, height=6)
par(mar=c(5, 4, 0.5, 0.5) + 0.1)
plot(white.hairs, bone.mineral.density, xlab = "Number of white hairs per square inch of scalp", ylab = "BMD (kg/m^3) [measure of osteoporosis]")
dev.off()


