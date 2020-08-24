# A vector of 50 normally distributed
# random numbers with a standard
# deviation of 5
N = 50
spread = 5
x = rnorm(N, sd=spread)

paste0('Standard deviation = ',
        round(sd(x), 3))
paste0('The variance is    = ',
        round(var(x), 3))
paste0('Square root of variance = ',
        round(sqrt(var(x)), 3))

# Run the code several times.