boards <- read.csv('/Users/kevindunn/ConnectMV/Datasets/Boards/all-thickness-values.csv')
nrow(boards)
ncol(boards)
boards[1:100,2:7]

plot(boards[1:100,5], type='l')
plot(boards[1:100,5], type='l')


# Number of board samples: 


# Show the data
boxplot(boards[1:100, 2:7], ylab="Board thickness (mils)")

boxplot(boards[1:100, 2:7], range=0, ylab="Board thickness (mils)")

#bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/boxplot-for-two-by-six-100-boards.png', type="png256", res=300, pointsize=14)
# Draw the boxplot
#dev.off()