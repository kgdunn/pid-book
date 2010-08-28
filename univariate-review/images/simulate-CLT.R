N = 500

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/simulate-CLT.png', type="png256", width=10, height=7, res=300, pointsize=14)

m <- t(matrix(seq(1,6), 3, 2))
layout(m)
s1 <- as.integer(runif(N, 1, 7))
s2 <- as.integer(runif(N, 1, 7))
s3 <- as.integer(runif(N, 1, 7))
s4 <- as.integer(runif(N, 1, 7))
s5 <- as.integer(runif(N, 1, 7))
s6 <- as.integer(runif(N, 1, 7))
s7 <- as.integer(runif(N, 1, 7))
s8 <- as.integer(runif(N, 1, 7))
s9 <- as.integer(runif(N, 1, 7))
s10 <- as.integer(runif(N, 1, 7))


hist(s1, main="", xlab="One throw")
bins = 8
hist((s1+s2)/2, breaks=bins, main="", xlab="Average of two throws")
hist((s1+s2+s3+s4)/4, breaks=bins, main="", xlab="Average of 4 throws")
hist((s1+s2+s3+s4+s5+s6)/6, breaks=bins, main="", xlab="Average of 6 throws")
bins=12
hist((s1+s2+s3+s4+s5+s6+s7+s8)/8,  breaks=bins, main="", xlab="Average of 8 throws")
hist((s1+s2+s3+s4+s5+s6+s7+s8+s9+s10)/10, breaks=bins, main="", xlab="Average of 10 throws")

dev.off()