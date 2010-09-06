function (df, nf = 2, rec = FALSE, niter = 100, tol = 1e-09) 
{
    df <- data.frame(df)
    tol <- 1e-09
    nc <- ncol(df)
    nr <- nrow(df)
    if (rec) 
        x <- list(li = matrix(0, nr, nf), c1 = matrix(0, nc, 
            nf), co = matrix(0, nc, nf), eig = rep(0, nf), nb = rep(0, 
            nf), rec = matrix(0, nr, nc))
    else x <- list(li = matrix(0, nr, nf), c1 = matrix(0, nc, 
        nf), co = matrix(0, nc, nf), eig = rep(0, nf), nb = rep(0, 
        nf))
    row.names(x$c1) <- names(df)
    row.names(x$co) <- names(df)
    row.names(x$li) <- row.names(df)
    cmeans <- colMeans(df, na.rm = TRUE)    
    csd <- apply(df, 2, sd, na.rm = TRUE) * (nr - 1)/nr
    X <- sweep(sweep(df, 2, cmeans, "-"), 2, csd, "/")
    x$tab <- X
    for (h in 1:nf) {
        th <- X[, 1]
        ph1 <- rep(1/sqrt(nc), nc)
        ph2 <- rep(1/sqrt(nc), nc)
        diff <- rep(1, nc)
        nb <- 0
        while (sum(diff^2, na.rm = TRUE) > tol & nb <= niter) {
            for (i in 1:nc) {
                the <- th[!is.na(X[, i])]
                ph2[i] <- sum(X[, i] * th, na.rm = TRUE)/sum(the * 
                  the, na.rm = TRUE)
            }
            ph2 <- ph2/sqrt(sum(ph2 * ph2, na.rm = TRUE))
            for (i in 1:nr) {
                ph2e <- ph2[!is.na(X[i, ])]
                th[i] <- sum(X[i, ] * ph2, na.rm = TRUE)/sum(ph2e * 
                  ph2e, na.rm = TRUE)
            }
            diff <- ph2 - ph1
            ph1 <- ph2
            nb <- nb + 1
        }
        if (nb > niter) 
            stop(paste("Maximum number of iterations reached for axis", 
                h))
        X <- X - th %*% t(ph1)
        x$nb[h] <- nb
        x$li[, h] <- th
        x$c1[, h] <- ph1
        x$eig[h] <- sum(th * th, na.rm = TRUE)/(nr - 1)
        x$co[, h] <- x$c1[, h] * sqrt(x$eig[h])
    }
    if (rec) {
        for (h in 1:nf) {
            x$rec <- x$rec + x$li[, h] %*% t(x$c1[, h])
        }
    }
    if (rec) {
        x$rec = as.data.frame(x$rec)
        names(x$rec) <- names(df)
        row.names(x$rec) <- row.names(df)
    }
    x$call <- match.call()
    x$nf <- nf
    class(x) <- "nipals"
    if (any(diff(x$eig) > 0)) 
        warning("Eigenvalues are not in decreasing order. Results of the analysis could be problematics")
    return(x)
}
