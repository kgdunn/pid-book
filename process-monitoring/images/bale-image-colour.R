
set.seed(42)
N = 5
samples = 100
raw.bale <- as.integer(runif(samples, 220, 255))
reshaped <- matrix(raw.bale, N, samples/N)

reshaped[1,14] <- 254
reshaped[2,14] <- 255
reshaped[3,14] <- 253
reshaped[4,14] <- 252
reshaped[5,14] <- 251

groups.S <- apply(reshaped, 2, sd)
groups.x <- round(apply(reshaped, 2, mean))


groups.x

xdb <- mean(groups.x)
s.bar <- mean(groups.S)

xdb
s.bar
an.5 = 0.940
LCL <- xdb - 3*s.bar/an.5/sqrt(N)
UCL <- xdb + 3*s.bar/an.5/sqrt(N)
c(LCL, UCL)
c(sum(groups.x<LCL), sum(groups.x>UCL))

bitmap('/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/bale-image-colour.png', type="png256", width=10, height=7, res=300, pointsize=14)
plot(groups.x, ylim=c(LCL-2, UCL+2), ylab="Subgroup averages (n=5)", xlab="Sequence order",  cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
abline(h=LCL, col="red")
abline(h=UCL, col="red")
dev.off()

# Now exclude that unusual column of data
# ------------------------------

reshaped <- reshaped[,-14]

groups.S <- apply(reshaped, 2, sd)
groups.x <- round(apply(reshaped, 2, mean))


groups.x

xdb <- mean(groups.x)
s.bar <- mean(groups.S)

xdb
s.bar
an.5 = 0.940
LCL <- xdb - 3*s.bar/an.5/sqrt(N)
UCL <- xdb + 3*s.bar/an.5/sqrt(N)
c(LCL, UCL)
c(sum(groups.x<LCL), sum(groups.x>UCL))


#library(qcc)