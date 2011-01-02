N = 2739
data <- cut (runif(N), 2)

bitmap('../images/histogram-children-by-gender.png', type="png256", 
    width=10, height=7, res=300, pointsize=14)
plot(data, xlab="Children born, by gender", ylab= paste("Number of children (N=", N, ")"),  
    names.arg=c("Male", "Female"), ylim=c(0, N/2+50), cex.axis=1.5, cex.lab=1.5, cex.names=1.5)
dev.off()