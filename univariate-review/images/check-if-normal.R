N = 100

bitmap('/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/check-if-normal.png', type="png256", width=10, height=7, res=300, pointsize=14)

s1 <- rf(N, 20, 20)
plot(s1, main="", xlab="A sequence of normal values?", ylab="",  cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.8, cex.axis=1.8)
write.table(s1, '/Users/kevindunn/Statistics course/Course notes/Univariate data analysis/images/check-if-normal.dat')
dev.off()