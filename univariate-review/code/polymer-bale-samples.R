data <- c(23, 19, 17, 18, 24, 26, 21, 14, 18)
N = length(data)

# Mean and standard deviation
data.mean <- mean(data)
data.sd <- sd(data)
cn <- qnorm(1 - 0.05/2)

# Assume we know sigma:
sigma <- 3.5
LB <- data.mean - cn * sigma / sqrt(N)
UB <- data.mean + cn * sigma / sqrt(N)
c(LB, UB) 
