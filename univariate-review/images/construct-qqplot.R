N = 10
index <- seq(1, N)
P <- (index - 0.5) / N
theoretical.quantity <- qnorm(P)


yields = c(86.2, 85.7, 71.9, 95.3, 77.1, 71.4, 68.9, 78.9, 86.9, 78.4)
mean.yield = mean(yields)		# 80.0
sd.yield = sd(yields)			# 8.35

yields.z = (yields - mean.yield)/sd.yield
# [1] 0.7425150  0.6826347 -0.9700599  1.8323353 -0.3473054 -1.0299401 -1.3293413 -0.1317365  0.8263473 -0.1916168

yields.z.sorted = sort(yields.z)
yields.z.sorted
#[1] -1.3376835 -1.0382915 -0.9784131 -0.3556777 -0.1999939 -0.1401155  0.6742308  0.7341092  0.8179390  1.8238961

theoretical.quantity
#[1] -1.6448536 -1.0364334 -0.6744898 -0.3853205 -0.1256613  0.1256613  0.3853205  0.6744898  1.0364334  1.6448536

plot(theoretical.quantity, yields.z.sorted, type="p")



norm <- rnorm(1000)
t <- rt(1000, df=3)
index = c(1, 2,3,4, seq(5, 95, 5), 96, 97, 98, 99)/100
norm.quantiles <- quantile(norm, index)
t.quantiles <- quantile(t, index)
plot(t.quantiles, norm.quantiles)