N = 1000
data <- cut (runif(N)*4-2, breaks=c(-2, -1, 0, +1, +2))

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/histogram-4-cuts.png', type="png256", res=300, pointsize=14)
plot(data, xlab="Defect type", ylab="Number of defects", names.arg=c("A", "B", "C", "D"), ylim=c(0, 0.3*N))
dev.off()