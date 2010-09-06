cheese <- read.csv('http://stats4.eng.mcmaster.ca/datasets/cheddar-cheese.csv')
library(car)

# Scatter plot matrix
# -----------------------
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/cheese-plots.png', type="png256", width=6, height=6, res=300, pointsize=14)
par(mar=c(1.5, 1.5, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
scatterplot.matrix(cheese[,2:5], col=c(1,1,1))
dev.off()

# Least squares model
# -----------------------
model.lm <- lm(cheese$Taste ~ cheese$Acetic + cheese$H2S + cheese$Lactic)
summary(model.lm)
RMSEE.lm <- sqrt(mean((cheese$Taste - predict(model.lm))**2))

# Least squares model: H2S
# -----------------------
model.lm.H2S <- lm(cheese$Taste ~  cheese$H2S )
summary(model.lm.H2S)
RMSEE.lm.H2S <- sqrt(mean((cheese$Taste - predict(model.lm.H2S))**2))

# Least squares model: lactic
# -----------------------
model.lm.lactic <- lm(cheese$Taste ~  cheese$Lactic )
summary(model.lm.lactic)
RMSEE.lm.lactic <- sqrt(mean((cheese$Taste - predict(model.lm.lactic))**2))

# Least squares model: acetic
# -----------------------
model.lm.acetic <- lm(cheese$Taste ~  cheese$Acetic )
summary(model.lm.acetic)
RMSEE.lm.acetic <- sqrt(mean((cheese$Taste - predict(model.lm.acetic))**2))

print(c(RMSEE.lm, RMSEE.lm.acetic, RMSEE.lm.H2S, RMSEE.lm.lactic))
# PCA model
# -----------------------
model.pca <- prcomp(cheese[,2:4], scale=TRUE)
summary(model.pca)

# PCR model
# -----------------------
P <- model.pca$rotation
T <- model.pca$x
model.pcr.1 <- lm(cheese$Taste ~ T[,1])
summary(model.pcr.1)
RMSEE.1 <- sqrt(mean((cheese$Taste - predict(model.pcr.1))**2))

model.pcr.2 <- lm(cheese$Taste ~ T[,1:2])
summary(model.pcr.2)

RMSEE.2 <- sqrt(mean((cheese$Taste - predict(model.pcr.2))**2))

c(RMSEE.lm, RMSEE.1, RMSEE.2)

# Plot observed against predicted
# -----------------------
plot(cheese$Taste, predict(model.pcr.2))
abline(lm(predict(model.pcr.2) ~ cheese$Taste -1))
