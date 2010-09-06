# 21 December 2009: preparation for class in 2010

library(car)
attach(Prestige)
some(Prestige)

#                    education income women prestige census type
#PURCHASING.OFFICERS     11.42   8865  9.11     56.8   1175 prof
#LAWYERS                 15.77  19263  5.13     82.3   2343 prof
#TELLERS.CASHIERS        10.64   2448 91.76     42.3   4133   wc
#TRAVEL.CLERKS           11.43   6259 39.17     35.7   4193   wc
#SALES.SUPERVISORS        9.84   7482 17.04     41.5   5130   wc
#ELECTRONIC.WORKERS       8.76   3942 74.54     50.8   8534   bc
#ELECTRICAL.LINEMEN       9.05   8316  1.34     40.9   8731   bc
#ELECTRICIANS             9.93   7147  0.99     50.2   8733   bc
#PLUMBERS                 8.33   6928  0.61     42.9   8791   bc
#TAXI.DRIVERS             7.93   4224  3.59     25.1   9173   bc

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-parametric-plots-without.png', type="png256", width=8, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)scatterplot(Prestige$income, Prestige$prestige, xlab="Average income ($)", ylab="Prestige", col=rep("black",5), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
plot(Prestige$income, Prestige$prestige, xlab="Average income ($)", ylab="Prestige",  cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
dev.off()

bitmap('/Users/kevindunn/Statistics course/Course notes/Correlation, covariance and least squares/images/non-parametric-plots-with.png', type="png256", width=8, height=7, res=300, pointsize=14)
par(mar=c(4.2, 4.2, 0.5, 0.5))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)scatterplot(Prestige$income, Prestige$prestige, xlab="Average income ($)", ylab="Prestige", col=rep("black",5), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")

scatterplot(Prestige$income, Prestige$prestige, xlab="Average income ($)", ylab="Prestige", col=rep("black",5), cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8, main="")
dev.off()