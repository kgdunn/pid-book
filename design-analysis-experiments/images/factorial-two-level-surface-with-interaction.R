
surface <- function(x1,x2){
    x1off = 360
    x1scale = 20
    x1s = (x1 - x1off)/x1scale
    
    x2off = 0
    x2scale = 1
    x2s = (x2 - x2off)/x2scale
    
    z = 30*x1s + 16*x2s- 10*x1s^2 - 20*x2s^2 +16*x1s*x2s + 40.1
}
surface.linear <- function(x1,x2){
    x1off = 395
    x1scale = 5
    x1s = (x1 - x1off)/x1scale
    
    x2off = (1.25+0.5)/2
    x2scale = (1.25-0.5)/2
    x2s = (x2 - x2off)/x2scale
    
    z = 2.5*x1s + 3.5*x2s +1.5*x1s*x2s + 81.5
}


Xoff = 360     # offset for X
Xscale = 20.0

N = 10 # resolution of surface
xlo = 390
xhi = 400
xmid = 395
ylo = 0.5
yhi = 1.25
ymid = (1.25+0.5)/2

x1 <- seq(xlo, xhi,length=N)
x2 <- seq(ylo , yhi, length=N)
g.linear <- expand.grid(x1=x1, x2=x2)
g.linear$y <- surface.linear(g.linear$x1, g.linear$x2)

g.actual <- expand.grid(x1=x1, x2=x2)
g.actual$y <- surface(g.actual$x1, g.actual$x2)


xlabels = c(xlo, xhi, xmid)
ylabels = c(ylo, yhi, ymid)
zmin = floor(surface(xlo,ylo))
zmax = floor(surface(xhi,yhi))

zlabels = c(zmin, 61, zmax)
g.actual$y[which.min(g.actual$y)] = zmin
#g$y[which.max(g$y)] = zmax

library(lattice)
png(file="/Users/kevindunn/Statistics course/Course notes/Design of experiments/images/factorial-two-level-surface-with-interaction.png", height = 1500, width = 1200, res=300, bg="transparent")
layout(matrix(c(1,2), 1, 2))
par.set <-  list(axis.line = list(col = "transparent"), clip = list(panel = "off"))
print(wireframe(y ~ x1*x2,
        data = g.linear,
        shade=TRUE,
        scales=list(arrows=FALSE,
                    distance=c(2,2.5,1),
                    rot=c(0),
                    x=list(draw=TRUE, at=xlabels, labels=as.character(xlabels), cex=1, rot=-45),
                    y=list(draw=TRUE, at=ylabels, labels=as.character(ylabels), cex=1, rot=30),
                    z=list(draw=TRUE, at=zlabels, labels=as.character(zlabels), cex=1)
                    ),
        aspect = c(0.9, 0.5),  # y/x and z/x
        par.settings = par.set,
        xlab="Temperature, T [K]",
        ylab=paste("Subtrate \n concentration\n S [g/L]"),
        zlab="Yield",
        alpha.regions = 0.2,
        #screen = list(z = 0, x = 45, y =45),
        )
)
print(wireframe(y ~ x1*x2,
        data = g.actual,
        shade=TRUE,
        scales=list(arrows=FALSE,
                    distance=c(2,2.5,1),
                    rot=c(0),
                    x=list(draw=TRUE, at=xlabels, labels=as.character(xlabels), cex=1, rot=-45),
                    y=list(draw=TRUE, at=ylabels, labels=as.character(ylabels), cex=1, rot=30),
                    z=list(draw=TRUE, at=zlabels, labels=as.character(zlabels), cex=1)
                    ),
        aspect = c(0.9, 0.5),  # y/x and z/x
        par.settings = par.set,
        xlab="Temperature, T [K]",
        ylab=paste("Subtrate \n concentration\n S [g/L]"),
        zlab="Yield",
        #screen = list(z = 0, x = 45, y =45),
)
)
dev.off()


Then manually crop the PNG output file