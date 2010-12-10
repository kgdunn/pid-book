salt <- c(460, 520, 580, 700, 760, 770, 890, 910, 920, 940, 960, 1060, 1100)
mean(salt)                                  # 813.077
median(salt)                                # 890
sd(salt)                                    # 202.0885
mad(salt)                                   # 192.738
1.4826*median(abs(salt - median(salt)))     # 192.738
IQR(salt)                                   # 240 = 940 - 700 (see below)
summary(salt) 
#   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 460.0   700.0   890.0   813.1   940.0  1100.0

bitmap('../images/soy-salt-content.png', type="png256", width=7, height=7, res=250, pointsize=14) 
boxplot(salt, ylab="Salt content (mg / 15mL serving)")
dev.off()

# Testing robustness.  Create an artificial outlier
# ------------------
salt[2] = 91941
mean(salt)                                  # 7845.462   <---- not robust at all
median(salt)                                # 910        <---- robust
sd(salt)                                    # 25268.22   <---- way off!
mad(salt)                                   # 222.39     <---- robust
1.4826*median(abs(salt - median(salt)))     # 222.39     <---- manual calculation of MAD
IQR(salt)                                   # 200        <---- robust
