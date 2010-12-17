snow <- c(170.9, 94.1, 138.0, 166.2, 175.8, 218.4, 56.6, 182.4, 243.2)
temp <- c(7.6,   8.8,  8.8,   7.3,   7.7,   8.2,   9.1 , 8.2,  7.7)
year <- seq(2000, 2008)

snow.long.average = 161.8
temp.long.average = 7.6

bitmap('../images/snowfall-data.png', type="png256", width=12, height=7, res=250, pointsize=14) 
plot(year, snow, xlab="Year", ylab="Snowfall (cm)", type="b")
abline(h=snow.long.average, col = "gray40")
text(2006, snow.long.average-5, "Total annual snowfall, averaged over 1971 to 2000 data")
dev.off()

bitmap('../images/temperature-data.png', type="png256", width=12, height=7, res=250, pointsize=14) 
plot(year, temp, xlab="Year", ylab="Average annual temperature (°C)", type="b")
abline(h=temp.long.average, col = "gray40")
text(2006, temp.long.average-0.1, "Average annual temperature, averaged over 1971 to 2000 data")
dev.off()