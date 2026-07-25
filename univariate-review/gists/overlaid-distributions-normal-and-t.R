# Overlay the normal distribution and the t-distribution
# for a sample of n = 7, so 6 degrees of freedom.
n <- 7
z <- seq(-5, 5, 0.01)
prob.norm <- dnorm(z)
prob.t <- dt(z, df=n-1)

plot(z, prob.norm, type="l", ylab="Normal and t-distributions", lwd=2)
lines(z, prob.t, lty=8, lwd=2)  # dashed line
legend(x=1.35, y=0.25, legend=c("Normal distribution", "t-distribution"),
       lty=c(1,8), lwd=c(2,2))
