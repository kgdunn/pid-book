B<-A<-c(-1, +1)
design <- expand.grid(A=A,B=B)
design$AB <- design$A * design$B
yield <- c(69, 60, 64, 53)
yield <- c(60, 72, 54, 68)
yield <- c(77, 79, 81, 89)

X = as.matrix(design)
X
mean(yield)
XtX <- t(X) %*% X
Xty <- t(X) %*% yield
XtX
Xty
solve(XtX)
solve(XtX) %*% Xty

#summary(model)


C<-T<-S<-c(-1, +1)
design <- expand.grid(C=C, T=T, S=S)
design$int = c(1, 1, 1, 1, 1, 1, 1, 1)
design$CT = design$C*design$T
design$CS = design$C*design$S
design$TS = design$T*design$S
design$CTS = design$C*design$T*design$S
yield <- c(77, 67, 28, 32, 75, 73, 29, 29)
#yield <- c(60, 72, 54, 68, 52, 83, 45, 80)
yield <- c(5, 30, 6, 33, 4, 3, 5, 4)

mean(yield)
X = as.matrix(design)
X
XtX <- t(X) %*% X

Xty <- t(X) %*% yield
XtX
Xty
solve(XtX) %*% Xty

model <- lm (yield ~ design$C + design$T + design$S + design$CT + design$TS + design$CS + design$CTS)
summary(model)


data =