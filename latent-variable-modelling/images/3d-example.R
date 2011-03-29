N = 100
x1 = rnorm(100, sd=5)
x2 = x1 + rnorm(100, sd=2)
x3 = 3*x1 + 2*x2 + rnorm(100, sd=1)
X <- data.frame(x1=x1, x2=x2, x3=x3)

library(lattice)

cube <- function(angle){
    # Plot rotating cube of the X values, at the given angle
    xlabels = 0
    ylabels = 0
    zlabels = 0
    lattice.options(panel.error=NULL) 
    par.set <-
        list(axis.line = list(col = "transparent"),
             clip = list(panel = "off"))

    print(
        cloud(
                X$x3 ~ X$x1 * X$x2,
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
                xlab=expression(paste("",  t[1], " "  )),
                ylab=expression(paste("",  t[2], " "  )),
                zlab="SPE",
                zoom = 0.95,
                
            )
        )            
}

X <- data.frame(x1=NA, x2=NA, x3=NA)
# Show the data cube, at an angle of 30 degrees
bitmap('3d-example-empty.png', type="png256", width=5, height=5, res=600, pointsize=14)
cube(30)
dev.off()

