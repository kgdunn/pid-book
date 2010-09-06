
set.seed(2)
N = 30

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/correlation-calculation.png', type="png256", width=14, height=14, res=300, pointsize=14)

layout(matrix(c(1,2,3, 4), 2,2))
par(mar=c(4.2, 4.2, 2, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)

x <- rnorm(N, mean=12, sd = 4)
y <- -4.2*x + rnorm(N, sd=8)
plot(x,y, main="A strong negative correlation", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
text(15, 0, paste("r(x,y) = ", round(cor(x, y),3)), cex=1.5)

x <- rnorm(N, mean=12, sd = 4)
y <- rnorm(N, mean=0, sd = 8)
plot(x,y, main="No correlation", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
text(7, -11, paste("r(x,y) = ", round(cor(x, y),3)), cex=1.5)

x <- rnorm(N, mean=, sd=9)
y <- (x)^2 + rnorm(N, mean=50, sd = 20)
plot(x, y, main="A relationship, but no correlation", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
text(10, 375, paste("r(x,y) = ", round(cor(x, y),3)), cex=1.5)

set.seed(4)
x <- rnorm(N, mean=, sd=9)
y <- 0.3*x +  rnorm(N, mean=50, sd = 4) + rt(N, df=4) + rf(N, df1=10, df2=10)
plot(x, y, main="A positive correlation", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
text(5, 40, paste("r(x,y) = ", round(cor(x, y),3)), cex=1.5)

dev.off()