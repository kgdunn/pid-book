thickness <- read.csv('/Users/kevindunn/ConnectMV/Datasets/Boards/all-thickness-values.csv')
summary(thickness)
thickness$t1.4 <- (thickness[,2] + thickness[,5])/2
thickness$t3.6 <- (thickness[,4] + thickness[,7])/2
thickness$diff <- (thickness[,2] + thickness[,3] + thickness[,4])/3  - (thickness[,5] + thickness[,6] + thickness[,7])/3
#plot(thickness$t1.4, thickness$tdiff)


X <- data.frame(x1=thickness$t1.4, x2=thickness$t3.6, x3=thickness$diff)
X <- X[seq(450,550),]

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/board-thickness-2d-plot.png', type="png256", width=6.6665, height=6.6665, res=300, pointsize=14)
par(mar=c(4.5, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.8, cex.sub=1.5, cex.axis=1.5)
plot(X[,1], X[,2], pch=20, cex=2, xlab="Tail thickness", ylab="Feed thickness")
dev.off()

library(lattice)

cube <- function(angle){
    # Plot a rotating cube of these thicknesses
    xlabels = 0
    ylabels = 0
    zlabels = 0
    lattice.options(panel.error=NULL) 
    par.set <-
        list(axis.line = list(col = "transparent"),
             clip = list(panel = "off"))

    print(
        cloud(
                X$x2 ~ X$x1 * X$x3,
                cex = 2, 
                type="p",
                pch=20,
                col="black",
                main="",
                screen = list(z = angle, x = -70, y = 0),                
             par.settings = par.set,
                scales = list(
                    col = "black", arrows=FALSE,
                    x=list(draw=FALSE, at=xlabels, labels=""),
                    y=list(draw=FALSE, at=ylabels, labels=""),
                    z=list(draw=FALSE, at=zlabels, labels=""),
                    distance=c(0.5,0.5,0.5)
                ),
                xlab="Tail thickness",
                ylab="Taper",
                zlab="Feed thickness",
                zoom = 0.95,
                
            )
        )            
}

jpeg(file='/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/board-thickness-3d-plot.png', height = 2000, width = 2000, quality=100, res=300)
cube(30)
dev.off()
