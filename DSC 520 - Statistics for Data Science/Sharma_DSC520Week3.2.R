# Assignment: ASSIGNMENT 3
# Name: Sharma, Vijay
# Date: 2024-12-12

# Read CSV file for American Community Survey

surveydata = read.csv("acs-14-1yr-s0201.csv")


# # There are 8 columns in the dataset and here are the details regarding # mean
# of data and what data type it can be in

# 1. Id - Identity column with varchar or string data type 
# 2. Id1 - Int column strip out of Id Column and should be an Integer data type # 3.
# 3. Geography - This is varchar or string type column showing city and county name
# 4. PopGroupId - This is Id column and should be shown as Integer. 
# 5. DisplayLabel(PopGroupId) - consider that as a string column 
# 6. RacesReported - Integer Data type column. 
# 7. HSDegree - Decimal Data type column 
# 8. BachDegree - Decimal Data type column


str(surveydata)

# nrow() function to show number of rows in surveydata
nrow(surveydata) 

# ncol() function to show number of columns in surveydata
ncol(surveydata)


# call ggplot2 library to plot histogram with HSDegree variable
library(ggplot2)

ggplot(surveydata) + 
  geom_histogram(mapping = aes(x = HSDegree, y = ..density..), fill = "steelblue", colour="black",binwidth = 2) +  # Plot the histogram with density on y-axis
  
  stat_function(fun = dnorm, args = list(mean = mean(surveydata$HSDegree), sd = sd(surveydata$HSDegree)), color = "red") +
  labs(title = "Distribution of High School Degree" , 
       x = "High School Degree Level",
       y = "Frequency") 

#Answers: 

# 1. This is not Unimodel Histogram
# 2. It is even not symmetrical
# 3. It is not bell shaped Too.
# 4. and not even normal distributed
# 5. It is definitely Skewed and in the the right direction.
# 6. Based on the histogram, a normal distribution cannot be accurately used as a model 
#for this data because the distribution is significantly skewed to the right, meaning there is #a long tail on the higher values, which is not characteristic of a normal distribution that 
# is symmetrical around the mean


# Probability plot for HSDegreee variable

qqnorm(surveydata$HSDegree) 
qqline(surveydata$HSDegree,col = "red")  # Adds a reference line to the plot [5, 8] 

#Answer the following questions based on the Probability Plot
# Based on what you see in this probability plot, is the distribution approximately normal? Explain how you know. 
#Answer: This is not normal distribution
# If not normal, is the distribution skewed? If so, in which direction? Explain how you know.

#Answer: - most of the data is not lying under straight line and it is mostly skewed in the middle in # probability curve

library (pastecs)
stat.desc (surveydata)


library (pastecs)
stat.desc (surveydata)

#In this distribution it is Positively Skewed and the values are more concentrated towards the #right side and the left tail is spread out. Hence, the statistical results are bent towards #the left-hand side. Hence, that the mean, median, and mode are always positive. In this #distribution, Mean >> Median >> Mode.

library(moments)

moments::skewness(surveydata$HSDegree)

#Negative skewness value indicates here that the distribution has a longer tail on the left side of the data, with most values clustered towards the higher end of the distribution.

moments::kurtosis(surveydata$HSDegree)

#Kurtosis is a statistical measurement that describes the shape of a distribution's peak and tails in relation to a normal distribution. 
#- A positive kurtosis value indicates that the distribution has a sharper peak and lower tails than a normal distribution. Generally Kurtosis more than 2 (positive) indicates a distribution is too peaked.