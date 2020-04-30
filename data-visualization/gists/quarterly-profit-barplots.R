labels = c("2008 Q1", "Q2", "Q3", "Q4",
            "2009 Q1", "Q2", "Q3", "Q4")
profit = c(45, 32, 67, 23, 42, 56, 64, 92)+40

# Draw a bar-plot
bp <- barplot(profit,
                names.arg=labels,
                axisnames=TRUE,
                ylab="Quarterly profit ($ '000)",
                border = TRUE)
text(bp, profit+3,
        labels=format(profit),
        xpd = TRUE,
        col = "black")

# Now rather use a line plot.
# Graph profit, but turn off axes
# and annotations
plot(profit, type="b", axes=TRUE,
        ann=FALSE, xaxt="n")

# Show the x-axis using our labels
axis(1, at=1:8, lab=labels)

# Plot title
title(ylab="Quarterly profit ($ '000)")