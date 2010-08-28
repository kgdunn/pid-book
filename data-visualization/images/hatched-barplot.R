# Found in example(barplot)

bitmap(file='/Users/kevindunn/Statistics course/Course notes/Visualization/images/hatched-barplot.png', type="png256", res=300, pointsize=14)

barplot(VADeaths, angle = 15+10*1:5, density = 20, col = "black", legend = rownames(VADeaths))
title(main = list("Death Rates in Virginia", font = 4))

dev.off()