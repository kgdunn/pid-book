N = 10
index <- seq(1, N)
P <- (index - 0.5) / N
theoretical.quantity <- qnorm(P)

yields = c(86.2, 85.7, 71.9, 95.3, 77.1, 71.4, 68.9, 78.9, 86.9, 78.4)
mean.yield = mean(yields)		# 80.0
sd.yield = sd(yields)			# 8.35
yields.z = (yields - mean.yield)/sd.yield
yields.z.sorted = sort(yields.z)

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/qqplot-derivation.png', type="png256", width=7, height=7, res=300, pointsize=14)
plot(theoretical.quantity, yields.z.sorted, type="p", cex.lab=1.5, cex.main=1.8, lwd=4, cex.sub=1.8, cex.axis=1.8)
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/qqplot-from-R.png', type="png256", width=7, height=7, res=300, pointsize=14)
qqnorm(yields, cex.lab=1.5, cex.main=1.5, lwd=2, cex.sub=1.5, cex.axis=1.5)
qqline(yields)
dev.off()
