rm <- read.csv('http://datasets.connectmv.com/file/raw-material-properties.csv')

ncol(rm)    # 7 columns
nrow(rm)    # 36 rows

# Plot the data as you normally would
plot(rm$size1, ylab="Particle size: level 1")

# Now use the identify(...) command, with the same data as you plotted. Use the
# "labels" option to let R use the "Sample" column to label points where you click
identify(rm$size1, labels=rm$Sample)
 
# After issuing the "identify(...)" command, click on any interesting points in the 
# plot.  Right-click anywhere to stop selecting points.


# Repeat with the other columns
plot(rm$size2, ylab="Particle size: level 2")
identify(rm$size2, labels=rm$Sample)
plot(rm$size3, ylab="Particle size: level 3")
identify(rm$size3, labels=rm$Sample)
plot(rm$density1, ylab="Particle density: level 1")
identify(rm$density1, labels=rm$Sample)
plot(rm$density2, ylab="Particle density: level 2")
identify(rm$density2, labels=rm$Sample)
plot(rm$density3, ylab="Particle density: level 3")
identify(rm$density3, labels=rm$Sample)
#-------- END OF CODE HERE

layout(matrix(seq(1,6), 2, 3))
plot(rm$size1, ylab="Particle size: level 1")
plot(rm$size2, ylab="Particle size: level 2")
plot(rm$size3, ylab="Particle size: level 3")
plot(rm$density1, ylab="Particle density: level 1")
plot(rm$density2, ylab="Particle density: level 2")
plot(rm$density3, ylab="Particle density: level 3")
