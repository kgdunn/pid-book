N = 100
data <- cut (runif(N), breaks=c(0, 0.7, 1.0))

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/histogram-70-30.png', type="png256", res=300, pointsize=14)
plot(data, xlab="Broken tablet production", ylab="Percentage of tablets", names.arg=c("Acceptable", "Broken"), ylim=c(0, 100))
dev.off()