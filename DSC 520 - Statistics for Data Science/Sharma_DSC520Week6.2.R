installed.packages("dpylr")
installed.packages("ggplot2")

library('dplyr')
library('ggplot2')

# Assign the iris dataset to a new variable called "my_iris"
my_iris <- iris 

## Average Sepal Length by Species
# Assuming your dataset is called "iris" 

my_iris %>% 
  group_by(Species) %>% 
  summarize(mean_sepal_length = mean(Sepal.Length))

## Visualizations

# Printing top 5 rows
head(my_iris,5)

sepal_length<-my_iris$Sepal.Length

sepal_width<-my_iris$Sepal.Width

hist(sepal_length,main="Histogram - Sepal Length",xlab="Sepal Length"
     ,breaks = 20, col="green",freq=FALSE)

hist(sepal_width,main="Histogram - Sepal Width",xlab="Sepal Width",xlim=c(2,5), 
     col="darkorchid",freq=FALSE)

# bar chart for average of the 4 quantitative variables
aveg<- apply(my_iris[,1:4], 2, mean)
barplot(aveg, ylab = "Average")

## box plot of multiple variables into one figure
boxplot(iris[,1:4], notch=T, col=c("red", "blue", "yellow", "grey"))

# set arrangement of multiple plots
par(mfrow=c(2,2))
# set margins
par(mar=c(4.5, 4.2, 3, 1.5)) 
hist(iris$Sepal.Length,xlab = "Sepal Length",cex.lab=1.5)
hist(iris$Sepal.Width,xlab = "Sepal Width",col="red")

boxplot(iris[,1]~iris[,5], notch=T, ylab="Sepal Length", col="blue")

# Here is analysis based on Visualization for different Species:

### The three Iris species clearly differ in their petal dimensions,with "setosa" 
### significantly shorter petals compared to both "versicolor" and "virginica.

# KEY POINTS :-
### 1. "versicolor" has slightly longer petals than "setosa". 
### 2. "virginica" stands out with notably longer and wider petals.
### 3. "setosa": Shortest petals.  
### 4. "versicolor":Moderately long petals,intermediate between"setosa"&"virgini"
### 5. "virginica": Longest and widest petals.