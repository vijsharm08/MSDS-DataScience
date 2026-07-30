## Negative or Left Skewness

x = rbeta(10000,5,2)
hist(x, main="Negative or Left Skewness", freq=FALSE)
lines(density(x), col='red', lwd=3)
abline(v = c(mean(x),median(x)),  col=c("green", "red"), lty=c(2,2), lwd=c(3, 3))

## Positive or Right Skewness

x = rbeta(10000,2,5)
hist(x, main="Positive or Right Skewness", freq=FALSE)
lines(density(x), col='red', lwd=3)
abline(v = c(mean(x),median(x)),  col=c("green", "red"), lty=c(2,2), lwd=c(3, 3))


## Symmetrical

x = rbeta(10000,5,5)
hist(x, main="Symmetrical", freq=FALSE)
lines(density(x), col='red', lwd=3)
abline(v = c(mean(x),median(x)),  col=c("green", "red"), lty=c(2,2), lwd=c(3, 3))

