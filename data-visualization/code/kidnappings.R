# Data from 1996 to 2007
bitmap('../images/kidnap-mobile.jpg', pointsize=14, res=300)
kidnap <- c(  4,   5, 6.5, 7.5, 8.75,   7,   7, 5, 3.25,    2, 1.5, 1.25)
mobile <- c(0.3, 0.4, 0.5, 0.6,  0.7, 0.8, 0.9, 2,  3.5, 4.25, 6.5, 7.25)
plot(mobile, kidnap, type='p', xlab="Mobile phone antennae [thousands]",
     ylab="Kidnappings per 100,000 residents")
dev.off()
