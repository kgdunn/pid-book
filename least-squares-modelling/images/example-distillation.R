dist <- read.csv('http://datasets.connectmv.com/file/distillation-tower.csv')

x <- dist$TempC2
y <- dist$VapourPressure 

model <- lm(log(y) ~ 1/x)

bitmap('../images/residual-plots.png', type="png256", width=14, height=7, res=300, pointsize=14)
layout(matrix(c(1,2), 1,2))
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
hist(model$residual, breaks=12, xlab="Model residuals", ylab="Freqency count",cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
library(car)
qq.plot(model$residuals, ylab="Model residuals")

dev.off()

# # breaks
# #  [1] -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
# # 
# # $counts
# #  [1]  6 11 20 40 29 19 38 26 27 18  7  4  3  2  2  0  0  0  0  0  1
# #  
# barplot(resid$intensities, names.arg=resid$mids, space=0.3, ylab="%", col="white", xlim=c(-6, 15))
# abline(v=0) 
# #axis(1, at=resid$mids, labels=as.character(resid$mids))
# #plot(years, bo, type="b",  ylim=c(0, 25), ylab="Breakouts per year", xlab="Year", cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.0, cex.axis=1, xaxt="n")
# 
# lines(lowess(resid$mids, resid$intensities))
# #,xaxs="r",xlim=c(.8,24.2))
#     text(x,u+.4,format(u,T))
#     lines(x[5:19],e-55,lwd=2)
#     points(x[5:19],e-55,lwd=2,cex=1.5,pch=1)
#     axis(4,seq(0,20,5),seq(55,75,5))
#     text(c(x[5],x[7],x[17],x[19]),c(e-55)[c(1,3,13,15)]+c(.5,-.7,-.7,.5),
#          format(c(e)[c(1,5,13,15)],T,di=3))
#     box()
#     dev.off()
