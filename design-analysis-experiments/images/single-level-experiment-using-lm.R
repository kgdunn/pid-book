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


lm_difference <- function(groupA, groupB)
{    
    # Build a linear model with groupA = 0, and groupB = 1
    
    y.A <- groupA[!is.na(groupA)]
    y.B <- groupB[!is.na(groupB)]
	x.A <- numeric(length(y.A))
	x.B <- numeric(length(y.B)) + 1
	y <- c(y.A, y.B)
	x <- c(x.A, x.B)
	x <- factor(x, levels=c("0", "1"), labels=c("A", "B"))
	
	model <- lm(y ~ x)
return(list(summary(model), confint(model)))
}


brittle <- read.csv('http://datasets.connectmv.com/file/brittleness-index.csv')
attach(brittle)  # Now we can access the variables directly, without $ symbols

group_difference(TK104, TK105)
lm_difference(TK104, TK105)

group_difference(TK104, TK107)
lm_difference(TK104, TK107)

group_difference(TK105, TK107)
lm_difference(TK105, TK107)

mano <- c(25,3,27,30,33,16,28,27,12,32,16)
dilt <- c(11,26,18,16,20,12,8,26,12,17,14)
group_difference(mano, dilt)
lm_difference(mano, dilt)
