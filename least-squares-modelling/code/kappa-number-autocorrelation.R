kappa <- read.csv('http://stats4.eng.mcmaster.ca/datasets/kappa-number.csv')
summary(kappa)
attach(kappa)
N = length(Kappa)

n.jumps = 5
sub = seq(1, N, n.jumps)
Kappa.sub <- Kappa[sub]

bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/kappa-number-autocorrelation.png', type="png256", width=14, height=14, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 3.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.8, cex.main=1.8, cex.sub=1.8, cex.axis=1.8 )
layout(matrix(seq(1, 2),2, 1))
acf(kappa, 50, main="Autocorrelation for the Kappa number variable", xlab="")
acf(Kappa.sub, 50, main="Autocorrelation of subsampled Kappa number vector")
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Assignments/Assignment 5/images/kappa-number-autocorrelation-scatterplots.png', type="png256", width=20, height=20/n.jumps, res=300, pointsize=14)
par(mar=c(4.2, 5, 3.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
par(cex.lab=1.5, cex.main=1.5, cex.sub=1.8, cex.axis=1.8 )


layout(matrix(seq(1, n.jumps+1),1, n.jumps+1))
for (jump in 0:n.jumps){
    
    plot(Kappa[seq(1,N-jump)], Kappa[seq(jump+1, N)], 
         xlab=paste("Kappa[seq(1, N-", substitute(jump, list(jump=jump)),")]", sep=""), 
         ylab=paste("Kappa[seq(", substitute(jump, list(jump=jump)), "+1,N)]", sep=""),
         main=paste("Subsample every ", substitute(jump, list(jump=jump)), " element")
    )
    lines(lowess(Kappa[seq(1,N-jump)], Kappa[seq(jump+1, N)]), col="red")
    
    correl = cor(Kappa[seq(jump+1, N)], Kappa[seq(1, N-jump)])
    correl = round(correl, 2)
    text(10, 35, paste("Correlation = ", substitute(correl, list(correl=correl)), "", sep=""), 
         pos=4, cex=1.3)
}
dev.off()