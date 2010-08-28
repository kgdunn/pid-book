labels = c("2008 Q1", "Q2", "Q3", "Q4", "2009 Q1", "Q2", "Q3", "Q4")
profit = c(45, 32, 67, 23, 42, 56, 64, 92)+40

bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/quarterly-profit-barplot-vs-lineplot.png', type="png256", height = 7, width = 14, res = 300, pointsize=12)

m <- t(matrix(1:2, 2, 1))
layout(m)

# Draw a bar-plot
bp <- barplot(profit, names.arg=labels, axisnames=TRUE, ylab="Quarterly profit ($ '000)", border = TRUE) #, axis.lty=1)
text(bp, profit+3, labels=format(profit), xpd = TRUE, col = "black")

# Now rather use a line plot
p_range = range(profit)
# Graph profit, but turn off axes and annotations
plot(profit, type="b", axes=TRUE, ann=FALSE, xlab="Quarter", xaxt="n")

# Make the x-axis using our labels
axis(1, at=1:8, lab=labels)

# Plot title
title(ylab="Quarterly profit ($ '000)")

dev.off()



bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/quarterly-profit-barplot-only.png', type="png256", height = 7, width = 7, res = 300, pointsize=12)

# Draw a bar-plot
bp <- barplot(profit, names.arg=labels, axisnames=TRUE, ylab="Quarterly profit ($ '000)", border = TRUE) #, axis.lty=1)
text(bp, profit+3, labels=format(profit), xpd = TRUE, col = "black")

dev.off()