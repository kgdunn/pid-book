spectra <- read.csv('/Users/kevindunn/Statistics course/Course notes/Latent variable modelling/images/spectral-data.csv', header=FALSE)
dim(spectra)
# 460 x 650

lvm <- prcomp(spectra, scale=TRUE, tol=1e-2)
A = 5
P <- lvm$rotation[,1:A]
T <- lvm$x[,1:A]

plot(P)

