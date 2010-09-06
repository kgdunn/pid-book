food <- read.csv('/Users/kevindunn/ConnectMV/Datasets/LDPE/food-texture.csv')

# Calculate the mean and standard deviation, ignoring missing values
food.mean <- apply(food, 2, mean, na.rm=TRUE)
food.sd <- apply(food, 2, sd, na.rm=TRUE)

# Remove the calculated mean (the statistic) from each column (margin=2)
# by using the subtract function (fun)
food.mc <- sweep(food, 2, food.mean)

# Scale each column, by dividing through by the standard deviation
food.mcuv <- sweep(food.mc, 2, food.sd, FUN='/')

# Now draw the boxplots
var.names <- colnames(food)

lvm <- prcomp(food, scale=TRUE)
P <- lvm$rotation
T <- lvm$x

# As you change "A", the variance is transferred between matrix E and Xhat
A <- 4
T <- as.matrix(food.mcuv) %*% P[,seq(1,A)]
Xhat <- T %*% t(P[,seq(1,A)])
E <- food.mcuv - Xhat

print (sum(food.mcuv * food.mcuv))
print (sum(Xhat * Xhat))
print (sum(E * E))

print (as.matrix(t(Xhat)) %*% as.matrix(E))