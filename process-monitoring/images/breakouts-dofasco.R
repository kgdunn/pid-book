
# Data from slides given to me by John MacGregor, 21 January 2010.  Used with permission.  (See directory "JFM notes")

# Accompanying text on the slide
# ------------------------------
#   * Significant reduction in breakouts over the past 10 years (since 1997)
#   * Several millions/year in reduced breakouts and increased productivity.

years <- seq(1988, 2006)
bo <- c(8,17, 23, 8, 12, 11, 17, 18, 18, 8, 9, 4, 4, 4, 7, 4, 2, 3, 2)

outputdir = '/Users/kevindunn/transfer/Stats-course/Course notes/Control charts/images/'
bitmap(paste(outputdir, 'breakouts-dofasco-economics.png', sep=""), type="png256", width=12, height=5, res=300, pointsize=14)
plot(years, bo, type="b",  ylim=c(0, 25), ylab="Breakouts per year", xlab="Year", cex.lab=1.5, cex.main=1.8, lwd=2, cex.sub=1.0, cex.axis=1, xaxt="n")
axis(1, at=years, labels=as.character(years))
abline(v=1997, col="grey70")
dev.off()

