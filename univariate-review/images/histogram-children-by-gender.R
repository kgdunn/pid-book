N = 2739
data <- cut (runif(N), 2)

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/histogram-children-by-gender.png', type="png256", width=10, height=7, res=300, pointsize=14)
plot(data, xlab="Children born, by gender", ylab= paste("Number of children (N=", N, ")"),  names.arg=c("Male", "Female"), ylim=c(0, N/2+50))
dev.off()