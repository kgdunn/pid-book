brittle <- read.csv('http://datasets.connectmv.com/file/brittleness-index.csv')
attach(brittle)  

# Calculates the paired difference
paired_difference <- function(groupA, groupB, alpha=0.95)
{    
    # This function assumes either group has missing data.  
    # Find the subset of observations in common.
    
    groupA.sub <- groupA[!is.na(groupA) & !is.na(groupB)]
    groupB.sub <- groupB[!is.na(groupA) & !is.na(groupB)]
    
    diffs <- groupB.sub - groupA.sub
    diffs.mean <- mean(diffs)
    diffs.sd <- sd(diffs)
    diffs.N <- length(diffs)
    
    plot(groupB.sub-groupA.sub, type="b")
    
    z <- (diffs.mean - 0) / (diffs.sd/sqrt(diffs.N))
    t.critical <- pt(z, df=(diffs.N-1))
    c.t <- qt(1-(1-alpha)/2, df=(diffs.N-1))
    LB <- diffs.mean  - c.t * diffs.sd / sqrt(diffs.N)
    UB <- diffs.mean  + c.t * diffs.sd / sqrt(diffs.N)
    
return(list(z, t.critical, diffs.N-1, LB, UB))
}

paired_difference(TK104, TK105, alpha=0.95)
# (z=2.64, t.critical=0.991, DOF=17, LB=9.81, UB=88.4)

paired_difference(TK104, TK107, alpha=0.95)
# (z=12, t.critical=1, DOF=19, LB=48.3, UB=68.7)

paired_difference(TK105, TK107, alpha=0.95)
# (z=-0.33, t.critical=0.37, DOF=20, LB=-46.1, UB=33.5)

# Use the built-in R function to get the same result:
t.test(TK104, TK107, paired=TRUE, mu=0, alternative="two.sided", var.equal=TRUE, conf.level=0.95)