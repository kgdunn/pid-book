stick <- function(x, y, pch=16, linecol=1, clinecol=1,...){
if (missing(y)){
    y = x
    x = 1:length(x) }
    plot(x,y,pch=pch, ...)
    for (i in 1:length(x)){
       lines(c(x[i],x[i]), c(0,y[i]),col=linecol)
    }
    lines(c(x[1]-2,x[length(x)]+2), c(0,0),col=clinecol)
}

N = 12

shewhart <- numeric(N)
shewhart[N] = 1

CUSUM <- (numeric(N)+1)*1/N

MA <- numeric(N)
MA[(N-4):N] = 0.2

EWMA <- numeric(N)
lambda <- 0.3
for (i in 1:N)
{
    EWMA[i] = lambda*(1-lambda)^(N-i)
}


bitmap('explain-weights-for-process-monitoring.png', type="png256", width=9, height=7, res=300, pointsize=14)

par(mfrow=c(2,2))
stick(shewhart, main=(expression(paste("Shewhart weights"))), ylim=c(0, 1), xaxt="n",  ylab="", xlab="")
axis(1, at=seq(1, 12), labels=c("", "", "", "", "", "...", "", "t-4", "", "t-2","", "t"), cex.lab=2)

stick(CUSUM, main=(expression(paste("CUSUM weights"))), ylim=c(0, 1), xaxt="n", xlab="", ylab="")
axis(1, at=seq(1, 12), labels=c("", "", "", "", "", "...", "", "t-4", "", "t-2","", "t"), cex.lab=2)

stick(MA, main=(expression(paste("MA weights when N=5"))), ylim=c(0, 1), xaxt="n", xlab="", ylab="")
axis(1, at=seq(1, 12), labels=c("", "", "", "", "", "...", "", "t-4", "", "t-2","", "t"), cex.lab=2)

stick(EWMA, main=(expression(paste("EWMA weights when "*lambda,' = ',0.3))), ylim=c(0, 1), xaxt="n", xlab="", ylab="")
axis(1, at=seq(1, 12), labels=c("", "", "", "", "", "...", "", "t-4", "", "t-2","", "t"), cex.lab=2)

dev.off()