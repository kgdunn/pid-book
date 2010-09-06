
surface <- function(x1,x2){
    x1off = 320
    x1scale = 20
    x1s = (x1 - x1off)/x1scale
    
    x2off = 0
    x2scale = 1
    x2s = (x2 - x2off)/x2scale
    
    z = 18*x1s + 10*x2s- 7*x1s^2 - 4*x2s^2 - 7.5*x1s*x2s + 60 
}

Xoff = 320     # offset for X
Xscale = 20.0

N = 50  # resolution of surface
x1 <- seq((338-Xoff)/Xscale, (354-Xoff)/Xscale ,length=N)*Xscale + Xoff
x2 <- seq(1.25 , 1.75, length=N)
g <- expand.grid(x1=x1, x2=x2)
g$y <- surface(g$x1, g$x2)

xlabels = c(338, 346, 354)
ylabels = c(1.25, 1.50, 1.75)
zmin = floor(surface(354,1.75))
zmax = ceiling(surface(338,1.25))
zlabels = c(zmin, 61, zmax)
g$y[which.min(g$y)] = zmin
g$y[which.max(g$y)] = zmax

library(lattice)
#png(file="/Users/kevindunn/Statistics course/Course notes/Design of experiments/images/factorial-two-level-surface-example.png", height = 1500, width = 1200, res=300, bg="transparent")

par.set <-  list(axis.line = list(col = "transparent"), clip = list(panel = "off"))
print(wireframe(y ~ x1*x2,
        data = g,
        shade=TRUE,
        scales=list(arrows=FALSE,
                    distance=c(2,2,1.5),
                    rot=c(30),
                    x=list(draw=TRUE, at=xlabels, labels=as.character(xlabels), cex=1, rot=-45),
                    y=list(draw=TRUE, at=ylabels, labels=as.character(ylabels), cex=1),
                    z=list(draw=TRUE, at=zlabels, labels=as.character(zlabels), cex=1)
                    ),
        aspect = c(0.9, 0.5),
        par.settings = par.set,
        xlab="Temperature, T [K]",
        ylab=paste("Subtrate \n concentration\n S [g/L]"),
        zlab="Yield",
)
)
dev.off()

Then manually crop the PNG output file