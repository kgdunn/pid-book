hurricane <- read.csv('http://datasets.connectmv.com/file/atlantic-hurricanes.csv')
nrow(hurricane)                             # 87 hurricanes in the data set

# We will do this manually.  You can use other R packages to do this
# more elegantlly though.
n.1950.1954 <- sum(hurricane$Year<1955) - sum(hurricane$Year<1950)
n.1955.1959 <- sum(hurricane$Year<1960) - sum(hurricane$Year<1955)
n.1960.1964 <- sum(hurricane$Year<1965) - sum(hurricane$Year<1960)
n.1965.1969 <- sum(hurricane$Year<1970) - sum(hurricane$Year<1965)
n.1970.1974 <- sum(hurricane$Year<1975) - sum(hurricane$Year<1970)
n.1975.1979 <- sum(hurricane$Year<1980) - sum(hurricane$Year<1975)
n.1980.1984 <- sum(hurricane$Year<1985) - sum(hurricane$Year<1980)
n.1985.1989 <- sum(hurricane$Year<1990) - sum(hurricane$Year<1985)
n.1990.1994 <- sum(hurricane$Year<1995) - sum(hurricane$Year<1990)
n.1995.1999 <- sum(hurricane$Year<2000) - sum(hurricane$Year<1995)
n.2000.2004 <- sum(hurricane$Year<2005) - sum(hurricane$Year<2000)
n.2004.2009 <- sum(hurricane$Year<2010) - sum(hurricane$Year<2005)

# Quick sanity check
nrow(hurricane) - sum(c(n.1950.1954, n.1955.1959, n.1960.1964, n.1965.1969, n.1970.1974, 
                        n.1975.1979, n.1980.1984, n.1985.1989, n.1990.1994, n.1995.1999, 
                        n.2000.2004, n.2004.2009)) == 0
                        
# The Poisson distribution is appropriate, parameters are eta = n * p = average number of events in the period
#
# Time period = 5 years
# Average number of events = mean(...) = 6.4
np <- mean(c(n.1950.1954, n.1955.1959, n.1960.1964, n.1965.1969, n.1970.1974, 
             n.1975.1979, n.1980.1984, n.1985.1989, n.1990.1994, n.1995.1999))


# Probability of 11 hurricanes in a 5 year period:
dpois(11, np)

# Probability of 0, 5, 20 hurricanes in a 5 year period:
dpois(c(0, 5, 20), np) * 100

x <- seq(0, 20)
plot(x, dpois(x, 6.4), xlab="Number of hurricanes", ylab="Probability of that many hurricanes", type="b")
