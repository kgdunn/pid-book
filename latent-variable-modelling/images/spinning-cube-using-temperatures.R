temps <- read.csv('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/room-temperature.csv', header=FALSE)
summary(temps)
plot(temps)
X <- data.frame(x1=temps$V1, x2=temps$V2, x3=temps$V3)

library(lattice)
# http://www.springer.com/statistics/computanional+statistics/book/978-0-387-75968-5

grouper = c(numeric(length=50)+1, numeric(length=10)+2, numeric(length=144-50-10)+1)
grouper[106] = 3

cube <- function(angle){
    # Plot a rotating cube of these thicknesses
    xlabels = 0
    ylabels = 0
    zlabels = 0
    lattice.options(panel.error=NULL) 
    print(cloud(
                 X$x3 ~ X$x1 * X$x2,
                 cex = 1, 
                 type="p",
                 groups = grouper,
                 pch=20,
                 col=c("black", "blue", "red"),
                 main="",
                 screen = list(z = angle, x = -70, y = 0),                
                 par.settings = list(axis.line = list(col = "transparent")), # causes cube to zoom in and out: clip = list(panel = "off")
                 scales = list(
                     col = "black", arrows=TRUE,
                     #x=list(draw=FALSE, at=xlabels, labels=""),
                     #y=list(draw=FALSE, at=ylabels, labels=""),
                     #z=list(draw=FALSE, at=zlabels, labels=""),
                     distance=c(0.5,0.5,0.5)
                 ),
                 xlab="x1",
                 ylab="x2",
                 zlab="x3",
                 zoom = 1.0
             )
        )  
}

angles = seq(0, 360, 1)
for(i in angles){
    
    if (i<10) {
        filename <- paste("frames/00", as.character(i), ".jpg", sep="")
    } else if (i<100) {
        filename <- paste("frames/0", as.character(i), ".jpg", sep="")
    } else {
        filename <- paste("frames/", as.character(i), ".jpg", sep="")
    }
        
    jpeg(file=filename, height = 1000, width = 1000, quality=100, res=300)#, bg="transparent")
    cube(i)
    dev.off()
}

system("ffmpeg -r 20 -b 1800 -i %03d.jpg animated-temperatures-with-colour-codes-1800.mp4")


# Code below: NOT USED ANYMORE
# 
# Then run these two lines at the command prompt
# ------------------------------------------------
# for f in *png ; do convert -quality 100 $f `basename $f png`jpg; done 
# mencoder "mf://*.jpg" -mf fps=2 -o test.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800 
#
# or
#