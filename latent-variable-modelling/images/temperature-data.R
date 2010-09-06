temps<- read.csv('http://stats4.eng.mcmaster.ca/datasets/room-temperature.csv')
temps

X <- data.frame(x1=temps$FrontLeft, x2=temps$FrontRight, x3=temps$BackLeft)


bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/temperature-2d-plot.png', type="png256", width=6.6665, height=6.6665, res=300, pointsize=14)
par(mar=c(4.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.5, cex.axis=1.5)
plot(X[,1], X[,2], pch=20, cex=2, xlab="Front left temperatures [K]", ylab="Back left temperatures [K]", xlim=c(290,299), ylim=c(290,299))
dev.off()


# Calculate the mean and standard deviation, ignoring missing values
temps.mean <- apply(temps, 2, mean, na.rm=TRUE)
temps.sd <- apply(temps, 2, sd, na.rm=TRUE)

# Remove the calculated mean (the statistic) from each column (margin=2)
# by using the subtract function (fun)
temps.mc <- sweep(temps, 2, temps.mean)

# Scale each column, by dividing through by the standard deviation
temps.mcuv <- sweep(temps.mc, 2, temps.sd, FUN='/')

model.pca <- prcomp(temps, scale=TRUE)
temps.P <- model.pca$rotation
temps.T <- model.pca$x

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/temperatures-first-loading.png', type="png256", width=10, height=4, res=300, pointsize=14)
par(mar=c(3.5, 4.2, 0.8, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.5, cex.axis=1.1)
barplot(temps.P[,1], col=0, ylim=c(-0.7, 0.7), ylab="Loadings: component 1")
abline(h=0)
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/temperatures-score-plot.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(5, 4.2, 4.0, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.5, cex.axis=1.1)
plot(temps.T[,1], temps.T[,2], xlab="Score 1", ylab="Score 2", main="Room temperature data")
abline(h=0, v=0)
dev.off()


A =1
temps.E.A <- temps.mcuv - as.matrix(temps.T[,1],N,A) %*% t(temps.P[,seq(1,A)])  # if A=1: 
SPE.A <- apply(temps.E.A ** 2, 1, sum)
reasonable.limit.95 = quantile(c(SPE.A[1:40], SPE.A[60:120]), 0.95)

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/temperatures-SPE-after-one-PC.png', type="png256", width=10, height=5, res=300, pointsize=14)
par(mar=c(4.0, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.3, cex.main=1.5, cex.sub=1.5, cex.axis=1.5)
plot(SPE.A, type='b', ylab="SPE after using 1 component", xlab="Time order")
abline(h=reasonable.limit.95, col='red')
dev.off()

library(lattice)

cube <- function(angle){
    # Plot a rotating cube of these thicknesses
    xlabels = 0
    ylabels = 0
    zlabels = 0
    lattice.options(panel.error=NULL) 
    par.set <-

    print(
        cloud(
                X$x3 ~ X$x1 * X$x2,
                cex = 2, 
                type="p",
                pch=20,
                col="black",
                main="",
                screen = list(z = angle, x = -70, y = 0),                
                par.settings = list(axis.line = list(col = "transparent"), clip = list(panel = "off")),
                scales = list(col = "black", arrows=TRUE,
                              distance=c(0.6,0.6,0.6)
                ),
                xlab="Front left",
                ylab="Front right",
                zlab="Back left",
                zoom = 1.035,
            )
        )            
}

jpeg(file='/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/temperature-3d-plot.png', height = 2000, width = 2000, quality=100, res=300)
cube(70)
dev.off()
