# We are going to be doing this 3 times. Rather write a function to 
# do the work for general "groupA" and "groupB" vectors.
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
    
    difference <- B.mean - A.mean
    var.DOF <- (A.N - 1 + B.N - 1)
    var.pooled <- ((A.N - 1) * A.var + (B.N - 1) * B.var) / var.DOF
    
    sd.denom <- sqrt(var.pooled *(1/A.N + 1/B.N))
    z <- (difference - 0) / sd.denom
    t.critical <- pt(z, var.DOF)
    
    LB <- difference - qt(0.975, df=var.DOF)*sd.denom
    UB <- difference + qt(0.975, df=var.DOF)*sd.denom
return(list(z, t.critical, LB, UB))
}

brittle <- read.csv('http://datasets.connectmv.com/file/brittleness-index.csv')
attach(brittle)  # Now we can access the variables directly, without $ symbols

# Let's start though by plotting boxplots of the data
bitmap('../images/brittleness-boxplot.png', type="png256", width=7, height=7, res=250, pointsize=14) 
par(mar=c(4.2, 4.2, 0.2, 0.2))  # (bottom, left, top, right); defaults are par(mar=c(5, 4, 4, 2) + 0.1)
boxplot(brittle, ylab="Brittleness index", cex.lab=1.5, cex.main=1.8, cex.sub=1.8, cex.axis=1.8)
dev.off()

# 104 vs 105
group_difference(TK104, TK105)
# z = 1.253729
# t.critical = 0.891298 (1-0.1087021)
# -31.4 < mu.diff < 134

# 104 vs 107
group_difference(TK104, TK107)
# z = 1.405639
# t.critical = 0.9163178 (1-0.0836822)
# -21.4 < mu.diff < 120

# 105 vs 107
group_difference(TK105, TK107)
# z = -0.05326222
# t.critical = 0.4788878 (1-0.5211122)
# -81.8 < mu.diff < 77.6