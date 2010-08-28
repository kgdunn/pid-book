boards <- read.csv('/Users/kevindunn/ConnectMV/Datasets/Boards/two-by-six-data.csv')

# Number of board samples: 
nrow(boards)

bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/boxplot-for-two-by-six-100-boards.png', type="png256", res=300, pointsize=14)

# Draw the boxplot
boxplot(boards[1:100,2:7], ylab="Board thickness (mils)")

dev.off()