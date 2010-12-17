# This was an alternative question: not used
# # Number of factors
# f <- ffDesMatrix(k=5)
# ff <- ffFullMatrix(f, x=c(1,2,3,4,5), 5)
# ff$Xa
# y <- c(61, 53, 63, 61, 53, 56, 54, 61, 69, 61, 94, 93, 66, 60, 95, 98, 56, 63, 70, 65, 59, 55, 67, 65, 44, 45, 78, 77, 49, 42, 81, 82)
# XtX <- t(ff$Xa) %*% ff$Xa
# Xty <- t(ff$Xa) %*% y
# b = solve(XtX) %*% Xty
# N = length(b)
# b.mod = abs(b[2:N])
# idx = order(b.mod)
# b.mod = b.mod[idx]
# labels=colnames(ff$Xa)[2:N]
# labels.mod = labels[idx]
# library(lattice)
# barchart(as.matrix(b.mod), ylab = "Effect", xlab="Magnitude of effect", scales=list(y=list(labels=labels.mod)), col=0)
# b
# library(car)
# qq.plot(b[2:N], labels=colnames(ff$Xa)[2:N])


# Number of factors
k = 4
library(BHH2)

# Generate the design matrix
f <- ffDesMatrix(k=k)

# Now expand this design matrix into the full X-matrix
full.X <- ffFullMatrix(f, x=seq(1,k), k)
X <- full.X$Xa

# Set the response values and solve for the standard full factorial model
y <- c(60, 59, 63, 61, 69, 61, 94, 93, 56, 63, 70, 65, 44, 45, 78, 77)
XtX <- t(X) %*% X
Xty <- t(X) %*% y
b = solve(XtX) %*% Xty
b
#               [,1]
# one         66.125
# x1          -0.625
# x2           9.000
# x3           4.000
# x4          -3.875
# x1*x2       -0.500
# x1*x3       -0.500
# x1*x4        0.875
# x2*x3        6.375
# x2*x4        1.250
# x3*x4       -5.250
# x1*x2*x3     1.125
# x1*x2*x4    -1.250
# x1*x3*x4     0.250
# x2*x3*x4    -0.125
# x1*x2*x3*x4  0.125

N = length(b)
b.mod = abs(b[2:N])
idx = order(b.mod)
b.mod = b.mod[idx]
labels=colnames(X)[2:N]
labels.mod = labels[idx]

bitmap('../images/bioreactor-pareto-plot.png', type="png256", width=8, height=8, res=300, pointsize=14)
library(lattice)
barchart(as.matrix(b.mod), ylab = "Effect", xlab="Magnitude of effect", 
         scales=list(y=list(labels=labels.mod)), col=0)
dev.off()

# Quickest way to select a subset of X
X.subset <- subset(X, select = c('one', 'x2', 'x3', 'x4', 'x2*x3', 'x3*x4'))

# More cumbersome and error prone, but works the same
sub.idx <- c(1, 3, 4, 5, 9, 11)
X.subset <- X[,sub.idx]

# We don't have to refit, but if we did, this is how one 
# can do it.  The b's are the same after refitting.
XtX <- t(X.subset) %*% X.subset
Xty <- t(X.subset) %*% y

# Now a 6 by 1 vector
b = solve(XtX) %*% Xty

y.hat = X.subset %*% b
e = y - y.hat
parameters = length(b)
n = length(y)
DOF = n - parameters
SE.model = sqrt(sum(e*e)/DOF)
c.t = qt(0.975, DOF)
S_E.b.i = sqrt(SE.model^2 / sum(X.subset[,2]^2))  # we could use any column of X though
conf.interval = c.t * S_E.b.i
c(SE.model, c.t, S_E.b.i, conf.interval)
data.frame(b, lower=b-conf.interval, upper=b+conf.interval)

# Half fraction
k = 4  # number of factors in factorial
f <- ffDesMatrix(k=k, gen=list(c(k, seq(1, k-1))))
#      [,1] [,2] [,3] [,4]
# [1,]   -1   -1   -1   -1
# [2,]    1   -1   -1    1
# [3,]   -1    1   -1    1
# [4,]    1    1   -1   -1
# [5,]   -1   -1    1    1
# [6,]    1   -1    1   -1
# [7,]   -1    1    1   -1
# [8,]    1    1    1    1

# Now expand this design matrix into the full X-matrix
full.X <- ffFullMatrix(f, x=seq(1,k), k)

# But we cannot estimate all 16 parameters, only select the 8 parameters of interest
X <- full.X$Xa[,c(1,2,3,4,5,6,7,8)]

# Select the rows from the full-y vector that correspond to the half-fraction
rows <- c(1, 10, 11, 4, 13, 6, 7, 16)
y <- y[rows]
XtX <- t(X) %*% X
Xty <- t(X) %*% y
b = solve(XtX) %*% Xty
b