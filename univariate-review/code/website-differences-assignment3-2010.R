# I used the same function in "brittleness-comparison-assignment3-2010.R"

group_difference <- function(groupA, groupB)
{    
    # This function assumes either group has missing data.  Calculate
    # the mean and variance omitting the missing values
    
    A.mean <- mean(groupA[!is.na(groupA)])
    A.var <- var(groupA[!is.na(groupA)])
    A.N <- length(groupA[!is.na(groupA)])

    B.mean <- mean(groupB[!is.na(groupB)])
    B.var <- var(groupB[!is.na(groupB)])
    B.N <- length(groupB[!is.na(groupB)])
    
    print(c(A.mean, B.mean, A.var, B.var, A.N, B.N))
    
    difference <- B.mean - A.mean
    var.DOF <- (A.N - 1 + B.N - 1)
    var.pooled <- ((A.N - 1) * A.var + (B.N - 1) * B.var) / var.DOF
    
    sd.denom <- sqrt(var.pooled *(1/A.N + 1/B.N))
    print(c(var.DOF, var.pooled, sd.denom))
    z <- (difference - 0) / sd.denom
    t.critical <- pt(z, var.DOF)
    
    LB <- difference - qt(0.975, df=var.DOF)*sd.denom
    UB <- difference + qt(0.975, df=var.DOF)*sd.denom
return(list(z, t.critical, LB, UB))
}

website <- read.csv('http://datasets.connectmv.com/file/website-traffic.csv')
attach(website)

visits.Mon <- Visits[DayOfWeek=="Monday"]
visits.Tue <- Visits[DayOfWeek=="Tuesday"]
visits.Wed <- Visits[DayOfWeek=="Wednesday"]
visits.Thu <- Visits[DayOfWeek=="Thursday"]
visits.Fri <- Visits[DayOfWeek=="Friday"]
visits.Sat <- Visits[DayOfWeek=="Saturday"]
visits.Sun <- Visits[DayOfWeek=="Sunday"]

# Look at a boxplot of the data from Friday and Saturday
bitmap('../images/website-boxplot.png', type="png256", width=7, height=7, res=250, pointsize=14) 
par(mar=c(4.2, 4.2, 0.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
boxplot(visits.Fri, visits.Sat, names=c("Friday", "Saturday"), ylab="Number of visits", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
dev.off()

# Use the "group_difference" function from question 4
group_difference(visits.Sat, visits.Fri)
# z = 3.104152
# t.critical = 0.9985255 (1-0.001474538)
# 1.953315 < mu.diff < 9.046685

t.test(visits.Sat, visits.Fri, alternative="two.sided", mu = 0, paired = FALSE, var.equal = TRUE, conf.level = 0.95)   # an alternative that gives the same results

all.visits <- cbind(visits.Mon, visits.Tue, visits.Wed, visits.Thu, visits.Fri, visits.Sat, visits.Sun)
all.visits[31, 5] = NA
all.visits[31, 6] = NA
all.visits[31, 7] = NA

risk <- matrix(nrow=7,ncol=7)
z <- matrix(nrow=7,ncol=7)
for (i in 1:7){
    for (j in 1:7){
        if (i>= j){
            out <- group_difference(all.visits[,i], all.visits[,j])
            z[i,j] = out[[1]]
        }
    }
}
print(z)

# All differences: z-values
# ----------------------------
#      Mon        Tue      Wed      Thu      Fri       Sat        Sun
# Mon  0.0000000        NA       NA       NA       NA        NA   NA
# Tue -0.2333225  0.000000       NA       NA       NA        NA   NA
# Wed -0.7431203 -0.496627 0.000000       NA       NA        NA   NA
# Thu  0.8535025  1.070370 1.593312 0.000000       NA        NA   NA
# Fri  2.4971347  2.683246 3.249602 1.619699 0.000000        NA   NA
# Sat  5.4320361  5.552498 6.151868 4.578921 3.104152  0.000000   NA
# Sun  3.9917201  4.141035 4.695493 3.166001 1.691208 -1.258885    0