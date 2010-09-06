T <- c(273, 285, 297, 309, 321, 333, 345, 357, 369, 381)
p <- c(1600, 1670, 1730, 1830, 1880, 1920, 2000, 2100, 2170, 2200)
h <- c(42, 48, 45, 49, 41, 46, 48, 48, 45, 49)

T.centered <- T - mean(T)
p.centered <- p - mean(p)
product <- T.centered * p.centered    # Note that R does element-by-element multiplication here
mean(product)
cov(T, p)
cor(T, p)
cor(T, h)


p.centered <- p - mean(p)
h.centered <- h - mean(h)
product <- h.centered * p.centered    
mean(product)
cov(p, h)


sum((T - mean(T)) * (p - mean(p)))

T.centered <- T - mean(T)
p.centered <- p - mean(p)
 
T.p.corr <- mean(T.centered * p.centered) / sqrt(sum((T - mean(T)) * (T - mean(T)))   *   sum((p - mean(p)) * (p - mean(p))) )
bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/cylinder-case-study.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(T, p, xlab="Temperature [K]", ylab="Pressure [kPa]", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
dev.off()

# Objective function plot
beta <- seq(5.3, 6.4, 0.08)
p <- c(1600, 1670, 1730, 1830, 1880, 1920, 2000, 2100, 2170, 2200)

ssq <- function(beta, temperature=c(273, 285, 297, 309, 321, 333, 345, 357, 369, 381))
{
    p.hat <- temperature*beta + 0
    error = p.hat - p
    ssq = sum(error*error)
    return(ssq)
}
obj <- sapply(beta, ssq)

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/cylinder-case-study-objective.png', type="png256", width=7, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 1.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
plot(beta, obj, ylab="Objective function value",  xlab=expression("b1"), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
dev.off()

