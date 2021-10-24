all.boards = read.csv("http://openmv.net/file/six-point-board-thickness.csv")
boards = all.boards[1:100, 2:7]

# Look at the start and end of the data
# Examine and summarize your data before
# doing anything else
head(boards)
tail(boards)

summary(boards)

boxplot(boards)
