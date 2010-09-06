food <- read.csv('/Users/kevindunn/ConnectMV/Datasets/LDPE/food-texture.csv')


bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-scatterplot-matrix.png', type="png256", width=14, height=9, res=300, pointsize=14)
library(car)
scatterplot.matrix(food, col=c(1,1,1,1,1))
dev.off()


# Calculate the mean and standard deviation, ignoring missing values
food.mean <- apply(food, 2, mean, na.rm=TRUE)
food.sd <- apply(food, 2, sd, na.rm=TRUE)

# Remove the calculated mean (the statistic) from each column (margin=2)
# by using the subtract function (fun)
food.mc <- sweep(food, 2, food.mean)

# Scale each column, by dividing through by the standard deviation
food.mcuv <- sweep(food.mc, 2, food.sd, FUN='/')

# Now draw the boxplots
var.names <- colnames(food)


bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-centering-and-scaling.png', type="png256", width=14, height=5, res=300, pointsize=14)
par(mar=c(8.5, 4.2, 4.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
layout(matrix(c(1,2,3),1,3))
boxplot(food, main="Raw data", xaxt="n")
axis(1, at=1:length(var.names), labels=var.names, las=2)
boxplot(food.mc, main="with mean centering", xaxt="n")
axis(1, at=1:length(var.names), labels=var.names, las=2)
boxplot(food.mcuv, main="centered and scaled to unit variance", xaxt="n")
axis(1, at=1:length(var.names), labels=var.names, las=2)
dev.off()


lvm <- prcomp(food, scale=TRUE)
names(lvm)
summary(lvm)
P <- lvm$rotation
T <- lvm$x

# Plot the loadings as a barplot
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-pc1-loadings.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
par(mar=c(3.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
barplot(lvm$rotation[,1], col=0, ylim=c(-0.7,0.7), width=1, ylab="1st component loadings")
abline(h=0)
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-pc2-loadings.png', type="png256", width=10, height=5.5, res=300, pointsize=14)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
par(mar=c(3.5, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
barplot(lvm$rotation[,2], col=0, ylim=c(-1,+1), width=1, ylab="2nd component loadings")
abline(h=0)
dev.off()

# Joint loadings plot:
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-both-loadings.png', type="png256", width=8, height=8, res=300, pointsize=14)
par(cex.lab=1.3, cex.main=1.3, cex.sub=1.3, cex.axis=1.3)
par(mar=c(5.0, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(lvm$rotation[,1], lvm$rotation[,2], xlim=c(-0.7,+0.7), ylim=c(-0.5,+1), pch=20, cex=2, xlab="1st component loadings [61%]", ylab="2nd component loadings [26%]")
text(lvm$rotation[,1], lvm$rotation[,2], var.names, cex = 1.0, pos=2, col = "black")
abline(h=0)
abline(v=0)
dev.off()

# Plot the scores in sequence order
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-pc1-scores.png', type="png256", width=8, height=4.5, res=300, pointsize=14)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
par(mar=c(4.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(lvm$x[,1], ylab="1st component scores", xlab="Sequence order", ylim=c(-4.3, 4.3))
abline(h=0)
dev.off()

# Plot the scores in sequence order
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-pc2-scores.png', type="png256", width=8, height=4.5, res=300, pointsize=14)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
par(mar=c(4.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(lvm$x[,2], ylab="2nd component scores", xlab="Sequence order", ylim=c(-2.5, 2.5))
abline(h=0)
dev.off()

# Joint score plot:
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-both-scores.png', type="png256", width=8, height=8, res=300, pointsize=14)
par(cex.lab=1.3, cex.main=1.3, cex.sub=1.3, cex.axis=1.3)
par(mar=c(5.0, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(lvm$x[,1], lvm$x[,2], xlim=c(-4,+4), ylim=c(-2.5, +2.5), pch=20, cex=2, xlab="1st component scores [61%]", ylab="2nd component scores [26%]")
text(lvm$x[,1], lvm$x[,2], seq(1, length(lvm$x[,1])), cex = 1.0, pos=4, col = "black")
abline(h=0)
abline(v=0)
dev.off()

# Contribution plot in t_1 for observation 33
bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/pca-on-food-texture-score-t1-contribution-for-obs-33.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(cex.lab=1.2, cex.main=1.3, cex.sub=1.3, cex.axis=1.3)
par(mar=c(2.5, 4.2, 1.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
obs_id = 33
a = 1
contribs <- as.matrix(food.mcuv[obs_id,] * P[,a])
print (food.mcuv[obs_id,])
print (P[,a])
barplot(contribs, names.arg=colnames(food.mcuv), col=0, ylim=c(-1.4,0),width=1, ylab="Contributions to t1 in observation 33")
abline(h=0)
dev.off()

system("python pca-on-food-texture-combine-plots.py")