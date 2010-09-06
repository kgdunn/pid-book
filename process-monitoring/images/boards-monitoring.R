boards <- read.csv('/Users/kevindunn/ConnectMV/Datasets/Boards/two-by-six-data.csv')
pos1 = boards$Pos1[1:10000]


N = length(pos1)
groups = 10

reshaped.data <- matrix(pos1, groups, N/groups)
blocked.means <- colMeans(reshaped.data)
blocked.median <- apply(reshaped.data, 2, median)

library(qcc)
qcc(blocked.means, type="xbar")
# qcc(diameter[1:25,], type="xbar", newdata=diameter[26:40,])
# q <- qcc(diameter[1:25,], type="xbar", newdata=diameter[26:40,], plot=FALSE)
# plot(q, chart.all=FALSE)
# qcc(diameter[1:25,], type="xbar", newdata=diameter[26:40,], nsigmas=2)
# qcc(diameter[1:25,], type="xbar", newdata=diameter[26:40,], confidence.level=0.99)
# 
# qcc(diameter[1:25,], type="R")
# qcc(diameter[1:25,], type="R", newdata=diameter[26:40,])
# 
# qcc(diameter[1:25,], type="S")
# qcc(diameter[1:25,], type="S", newdata=diameter[26:40,])