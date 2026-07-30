---
  title: "Sharma_DSC520Week11.2"
output: pdf_document
date: "2025-02-18"
---
install.packages("class")
install.packages("rattle")


library(class)
library(dplyr)
library(stats)
library(ggplot2)
library(caTools)
library(rattle)
library(cluster)


# Set working directory for this week assignment data

## Pulling the Data frame for the binary-classifier data as below.
binary_classifier_data <- read.csv('binary-classifier-data.csv')
head(binary_classifier_data)

## Next I will be pulling the data for the trinary-classifier data as below.
trinary_classifier_data <- read.csv('trinary-classifier-data.csv')
head(trinary_classifier_data)

#Plot the data from each dataset using a scatter plot.

## Created a scatter plot for the binary_classifier_data frame
ggplot(binary_classifier_data,aes(x,y,color=label)) + 
  geom_point() + 
  scale_color_gradient2(low="white", mid="green", high="purple")

## Next I created a scatter plot for the trinary_classifier_data frame
ggplot(trinary_classifier_data, aes(x,y,color=label)) + 
  geom_point() + 
  scale_color_gradient2(low="white", mid="magenta", high="black")

# The k nearest neighbors algorithm categorizes an input value by looking at the 
# labels for the k nearest points and assigning a category based on the most 
# common label. In this problem, you will determine which points are nearest by 
# calculating the Euclidean distance between two points. As a refresher, 
# the Euclidean distance between two points:

# First I will create data normalization for both bindary and trinary data frames.
binary <- binary_classifier_data[, c("x", "y")]
trinary <- trinary_classifier_data[, c("x", "y")]

# Next I will create my train and test data sets for both binary and 
# trinary data frames.train and test data sets for binary data and pull the 
# number of observations for the binary train and test data
set.seed(150)
binary_selection<-sample(1:nrow(binary),size=nrow(binary)*0.60, replace = FALSE)
binary_train <- binary_classifier_data[binary_selection,]
NROW(binary_train)

binary_test <- binary_classifier_data[-binary_selection,]
NROW(binary_test)

# Next I will create dataframes for both train and test label data for the 
# binary data and pull the number of observations for the binary train 
train_label_binary <- binary_classifier_data[binary_selection,1,drop=TRUE]
NROW(train_label_binary)

test_label_binary <- binary_classifier_data[-binary_selection,1,drop=TRUE]
NROW(test_label_binary)

# train and test data sets for trinary data and pull the number of observations 
# for the trinary train and test data
set.seed(130)
trinary_selection<-sample(1:nrow(trinary),
                          size=nrow(trinary)*0.60,replace = FALSE)
trinary_train <- trinary_classifier_data[trinary_selection,]
NROW(trinary_train)

trinary_test <- trinary_classifier_data[-trinary_selection,]
NROW(trinary_test)

# Next I will create dataframes for both train and test label data for the 
# trinary data and pull the number of observations for the trinary and test data
train_label_trinary <- trinary_classifier_data[trinary_selection,1,drop=TRUE]
NROW(train_label_trinary)

test_label_trinary <- trinary_classifier_data[-trinary_selection,1,drop=TRUE]
NROW(test_label_trinary)

# Fit a k nearest neighbors’ model for each dataset for k=3, k=5, k=10, k=15, 
# k=20, and k=25. Compute the accuracy of the resulting models for each value of 
# k.Plot the results in a graph where the x-axis is the different values of k and 
# the y-axis is the accuracy of the model.

# Fitting a model is when you use the input data to create a predictive model. 
# There are various metrics you can use to determine how well your model fits  
# data. For this problem, you will focus on a single metric, accuracy. 
# Accuracy is simply the percentage of how often the model predicts the correct 
# result. If the model always predicts the correct result, it is 100% accurate. 
# If the model always predicts the incorrect result, it is 0% accurate.

# Create a K nearest list the k nearest neighbors for binary data.
k_nearest <- list(3,5,10,15,20,25)
input=1
binary_accuracy=1
for (input in k_nearest) 
{
  nearest_neighbor <- knn(train = binary_train, 
                          test = binary_test, 
                          cl=train_label_binary, 
                          k=input)
  binary_accuracy[input] <- 100*
    sum(test_label_binary == nearest_neighbor)/NROW(test_label_binary)
  k=input
  cat(k,'=',binary_accuracy[input],'')
}

# Next I will plot the accuracy of my k values for binary
plot(binary_accuracy, type = "b", xlab = "k Nearest Neighbors Value", 
     ylab = "Level of Accuracy")


# Create a K nearest list the k nearest neighbors for trinary data. 
k_nearest_trinary <- list(3,5,10,15,20,25)
input_trinary=1
trinary_accuracy=1
for (input_trinary in k_nearest_trinary) 
{
  trinary_nearest <- knn(train = trinary_train, 
                         test = trinary_test, 
                         cl=train_label_trinary, 
                         k=input_trinary)
  trinary_accuracy[input_trinary] <- 100*
    sum(test_label_trinary == trinary_nearest)/NROW(test_label_trinary)
  k=input_trinary
  cat(k,'=',trinary_accuracy[input_trinary])
}

# Next I will plot the accuracy of my k values for binary
plot(trinary_accuracy, type = "b", 
     xlab = "k Nearest Neighbors Value", 
     ylab = "Level of Accuracy")  
k=input_trinary
cat(k,'=',trinary_accuracy[input_trinary])

# Looking back at the plots of the data, do you think a linear classifier would 
# work well on these datasets? yes I believe so as a linear classifier can 
# classify data into labels based on a linear combination of input features
# How does the accuracy of your logistic regression classifier from last week 
# compare? Why is the accuracy different between these two methods?
# The accuracy from this weeks method shows that for our trinary data that our 
# accuracy went down as the k value went up as seen in our graph and outputs. 
# While in our binary data we saw that as the k value increased the accuracy 
# decreased as well but at a higher scale.

## Pulling the Data frame for the clustering_data as seen below.
clustering_data <- read.csv('clustering-data.csv')
head(clustering_data)

# Plot the dataset using a scatter plot.

## Created a scatter plot for the binary_classifier_data frame
ggplot(clustering_data, aes(x=clustering_data$x, y=clustering_data$y)) + 
  geom_point()

# Fit the dataset using the k-means algorithm from k=2 to k=12. 
# Create a scatter plot of the resultant clusters for each value of k.

head(clustering_data)

# standardize the variable
clust_standard <- scale(clustering_data[-1])
# k-means from k=2 to k=12
clust_k_means_fit <- kmeans(clust_standard, 4)
# collect attributes
attributes(clust_k_means_fit)

# view the centroids 
clust_k_means_fit$centers

# view the clusters
clust_k_means_fit$cluster

# create the cluster
clust_nearest <- list(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
clust_input = 1
seed = 1234
nc = 12
clustplot <- function(clustering_data, nc=12, seed=1234)
{ 
  clustss <- (nrow(clustering_data)-1)*sum(apply(clustering_data,2,var)) 
  
  for (clust_input in 2:nc) 
  {
    set.seed(seed)
    clustss[clust_input] <-sum(kmeans(clustering_data, 
                                      centers = clust_input)$withinss)
  }
  
  # Plot my cluster using the plot function
  plot(1:nc, clustss, type="b", 
       xlab="number of clusters", 
       ylab="Within groups sum of squares")
}

# As seen in our graph that was generated in the previous example we see that 
# our elbow point was at 4
clustplot(clust_standard, nc =4)

# Next I will create a cluster plot to see the best value

# use the function clustplot to plot our findings
clusplot(clust_standard, 
         clust_k_means_fit$cluster, 
         main = 'cluster solutions', 
         color = TRUE, shade = TRUE, labels = 2, lines = 0)

# As k-means is an unsupervised algorithm, you cannot compute the accuracy as 
# there are no correct values to compare the output to. Instead, you will use the 
# average distance from the center of each cluster as a measure of how well the 
# model fits the data. To calculate this metric, simply compute the distance of 
# each data point to the center of the cluster it is assigned to and take the 
# average value of all of those distances.

# I will calculate the distance between and plot 
clust_dist <- dist(clust_standard)
# create hclust for different methods
clust_complete <- hclust(clust_dist, method = "complete")
clust_single <- hclust(clust_dist, method = "single")
clust_average <- hclust(clust_dist, method = "average")
# plot data
par(mfrow= c(1,3))
plot(clust_complete, main = 'Complete link')
plot(clust_single, main = 'Single link')
plot(clust_average, main = 'Average link')
