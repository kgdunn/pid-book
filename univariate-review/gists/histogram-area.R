# 1000 normally distributed values
N <- 1000
values <- rnorm(N)
hist(values, freq=TRUE,  xlab="Random values",
        cex.lab=1.5, cex.main=1.8, lwd=2,
        cex.sub=1.8, cex.axis=1.8,
        ylab=paste0("Frequency (N=",N,")"))
hist(values, freq=FALSE, xlab="Random values",
        cex.lab=1.5, cex.main=1.8, lwd=2,
        cex.sub=1.8, cex.axis=1.8,
        ylab="Relative density")

# Compare the two plots: only the y-axis
# changes but the general shape remains.