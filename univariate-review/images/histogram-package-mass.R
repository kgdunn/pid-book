data <- rnorm(500, mean=1100, sd=50)

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/histogram-package-mass-1.png', type="png256", width=10, height=7, res=300, pointsize=14)
hist(data, xlab="Mass [g] of each package", ylab="Number of packages (N=500)")
dev.off()