library(lattice)  

#  Comment these two lines to get the colour version
ltheme <- canonical.theme(color = TRUE)
ltheme$strip.background$col <- "white" ## change strip bg  
lattice.options(default.theme = ltheme) 


super.sym <- trellis.par.get("superpose.symbol")
super.sym$pch[1:3] <- c(1,2,3)

bitmap('/Users/kevindunn/Statistics course/Course notes/Latent-variable-modelling/images/brushing-illustration-colour.png', type="png256", width=6, height=6, res=300, pointsize=14)

splom(~iris[1:4], groups = Species, data = iris,
      panel = panel.superpose,
      pscales = 0,
      auto.key = list(columns = 3, title = "Species"),
      key = list(title = "Three Varieties of Iris",
                 columns = 3, 
                 points = list(pch = super.sym$pch[1:3],
                 col = super.sym$col[1:3]),
                 text = list(c("Setosa", "Versicolor", "Virginica"))))
                 
dev.off()