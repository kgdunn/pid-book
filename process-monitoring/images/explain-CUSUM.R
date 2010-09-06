

set.seed(-92)

steps <- seq(0, 200)
N <- length(steps)

base.sd <- 3
base.mean <- 20
target <- base.mean

data <- rnorm(N, base.mean, base.sd)


bitmap('/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/explain-CUSUM.png', type="png256", width=20, height=25, res=300, pointsize=14)

m <- t(matrix(seq(1,4), 1, 4))
layout(m)

plot(data, type="p", pch=".", cex=10, cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, xlab="", ylab="", main="Raw data: no shift in mean")
abline(h=base.mean, col="grey80")
points(data, type="p",pch=".", cex=10)

S <- numeric(N)   # create a vector of zeros
S[1] = data[1] - target
for (k in 2:N)
{
   S[k] <- S[k-1] + data[k] - target
}
range(S)
plot(S, type="b", cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, xlab="Time steps", ylab="", main="S(t)", ylim=c(-20, 120))
abline(h=0)
x=170
d = 10
angle = 30
vert = 15
arrows(x0=x+d, y0=S[x], x1=x-10, y1=S[x]-angle, col="red", code=0, lwd=2)
arrows(x0=x+d, y0=S[x], x1=x-10, y1=S[x]+angle, col="red", code=0, lwd=2)
arrows(x0=x, y0=S[x]-vert, x1=x, y1=S[x]+vert, col="red", code=0, lwd=2)



# Now add a shift to the data
# ----------------------------
step.point <- 150
step.fraction <- 0.4
data.shift <- data
data.shift[step.point:N] <- data.shift[step.point:N] + step.fraction*base.sd

plot(data.shift, type="p", pch=".", cex=10, cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, xlab="", ylab="", main="A shift of 1.2 units (0.4 sigma) at t=150")
abline(h=base.mean, col="grey80")


S.shift <- numeric(N)   # create a vector of zeros
S.shift[1] = data.shift[1] - target
for (k in 2:N)
{
   S.shift[k] <- S.shift[k-1] + data.shift[k] - target
}
plot(S.shift, type="b", cex.lab=1.5, cex.main=3, cex.sub=3, cex.axis=3, xlab="Time steps", ylab="", main="S(t)", ylim=c(-20, 120))
abline(h=0)



x=170
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]-angle, col="red", code=0, lwd=2)
arrows(x0=x+d, y0=S.shift[x], x1=x-10, y1=S.shift[x]+angle, col="red", code=0, lwd=2)
arrows(x0=x, y0=S.shift[x]-vert, x1=x, y1=S.shift[x]+vert, col="red", code=0, lwd=2)

dev.off()