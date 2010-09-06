dist <- read.csv('http://stats4.eng.mcmaster.ca/datasets/distillation-tower.csv')
X <- as.matrix(dist[,2:28])
X.mean <- apply(X, 2, mean, na.rm=TRUE)
X.mc <- sweep(X, 2, X.mean)
X.scale <- apply(X.mc, 2, sd, na.rm=TRUE)
X.mcuv <- sweep(X.mc, 2, X.scale, FUN='/')
XtX <- t(X.mcuv) %*% X.mcuv
ev <- eigen(XtX, symmetric=TRUE)
ev$sum <- sum(ev$values)
K <- 10
library(lattice)

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/eigenvalue-scree-plot.png', type="png256", width=10, height=5, res=300, pointsize=14)
barchart(as.matrix(ev$values[1:K] / ev$sum * 100), horizontal=FALSE, col=0, ylab=list(label="Proportion of variance explained (%)", cex=1.5), xlab=list(label="Component number", cex=1.5), scales=list(x=list(labels=seq(1,K), cex=1.5), y=list(cex=1.5))  )
dev.off()