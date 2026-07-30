# ==============================================================================
# Kia/Hyundai Vehicle Theft Crisis: A Data Story
# Author: Data Analysis Project
# Date: January 2026
# ==============================================================================
# PURPOSE: Analyze and visualize the Kia/Hyundai vehicle theft epidemic
#          across multiple U.S. cities to inform policymakers and the public
# ==============================================================================

install.packages("dplyr")

# Load required libraries

library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(treemapify)
library(lubridate)
library(RColorBrewer)
library(gridExtra)

# ==============================================================================
# DATA LOADING
# ==============================================================================

getwd()

# Load all three datasets

kia_hyundai_thefts <- read.csv('/Users/vijsharm/kiaHyundaiThefts.csv')

milwaukee_data <- read.csv('KiaHyundaiMilwaukeeData.csv')

car_thefts_map <- read.csv('carTheftsMap.csv')



# ==============================================================================

# DATA PREPARATION

# ==============================================================================



# Create a date column for time series analysis

kia_hyundai_thefts$date <- as.Date(paste(kia_hyundai_thefts$year,
                                         
                                         kia_hyundai_thefts$month,
                                         
                                         "01", sep="-"),
                                   
                                   format="%Y-%b-%d")



milwaukee_data$date <- as.Date(paste(milwaukee_data$year,
                                     
                                     milwaukee_data$month,
                                     
                                     "01", sep="-"),
                               
                               format="%Y-%b-%d")



# Calculate total thefts for each city

city_totals <- kia_hyundai_thefts %>%
  
  group_by(city, state) %>%
  
  summarise(
    
    total_kia_hyundai = sum(countKiaHyundaiThefts, na.rm = TRUE),
    
    total_other = sum(countOtherThefts, na.rm = TRUE),
    
    avg_percent_kia_hyundai = mean(percentKiaHyundai, na.rm = TRUE)
    
  ) %>%
  
  arrange(desc(total_kia_hyundai))



# Add total thefts column

city_totals$total_all_thefts <- city_totals$total_kia_hyundai + city_totals$total_other



# Calculate yearly totals across all cities

yearly_totals <- kia_hyundai_thefts %>%
  
  group_by(year) %>%
  
  summarise(
    
    kia_hyundai = sum(countKiaHyundaiThefts, na.rm = TRUE),
    
    other = sum(countOtherThefts, na.rm = TRUE)
    
  )



# Prepare data for stacked area chart

monthly_aggregate <- kia_hyundai_thefts %>%
  
  group_by(date) %>%
  
  summarise(
    
    kia_hyundai_thefts = sum(countKiaHyundaiThefts, na.rm = TRUE),
    
    other_thefts = sum(countOtherThefts, na.rm = TRUE)
    
  ) %>%
  
  arrange(date)



# ==============================================================================

# VISUALIZATION 1: PIE CHART - Top 5 Cities by Total Kia/Hyundai Thefts

# ==============================================================================



# Prepare data for pie chart (Top 5 cities + Others)

top5_cities <- city_totals %>%
  
  top_n(5, total_kia_hyundai) %>%
  
  mutate(city_label = paste(city, state, sep = ", "))



other_cities_sum <- city_totals %>%
  
  filter(!city %in% top5_cities$city) %>%
  
  summarise(total_kia_hyundai = sum(total_kia_hyundai)) %>%
  
  mutate(city_label = "Other Cities")



pie_data <- bind_rows(
  
  top5_cities %>% select(city_label, total_kia_hyundai),
  
  other_cities_sum
  
)



# Calculate percentages for labels

pie_data <- pie_data %>%
  
  mutate(
    
    percentage = total_kia_hyundai / sum(total_kia_hyundai) * 100,
    
    label = paste0(city_label, "\n",
                   
                   format(total_kia_hyundai, big.mark = ","),
                   
                   " (", round(percentage, 1), "%)")
    
  )



# Create pie chart

pie_chart <- ggplot(pie_data, aes(x = "", y = total_kia_hyundai, fill = city_label)) +
  
  geom_bar(stat = "identity", width = 1, color = "white", size = 1.2) +
  
  coord_polar("y", start = 0) +
  
  geom_text(aes(label = paste0(round(percentage, 1), "%")),
            
            position = position_stack(vjust = 0.5),
            
            color = "white", fontface = "bold", size = 4) +
  
  scale_fill_brewer(palette = "Set1") +
  
  theme_void() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    legend.position = "right",
    
    legend.title = element_text(face = "bold"),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Distribution of Kia/Hyundai Thefts by City (2019-2022)",
    
    subtitle = "Chicago accounts for nearly half of all reported thefts",
    
    fill = "City"
    
  )



# Save the plot

ggsave("1_pie_chart_cities.png", pie_chart, width = 10, height = 7, dpi = 300)

print(pie_chart)



# ==============================================================================

# VISUALIZATION 2: DONUT CHART - Kia/Hyundai vs Other Vehicle Thefts (2022)

# ==============================================================================



# Prepare data for 2022

theft_type_2022 <- kia_hyundai_thefts %>%
  
  filter(year == 2022) %>%
  
  summarise(
    
    `Kia/Hyundai` = sum(countKiaHyundaiThefts, na.rm = TRUE),
    
    `Other Vehicles` = sum(countOtherThefts, na.rm = TRUE)
    
  ) %>%
  
  pivot_longer(cols = everything(), names_to = "type", values_to = "count")



# Calculate percentages

theft_type_2022 <- theft_type_2022 %>%
  
  mutate(
    
    percentage = count / sum(count) * 100,
    
    ymax = cumsum(percentage),
    
    ymin = c(0, head(ymax, n = -1)),
    
    label_position = (ymax + ymin) / 2
    
  )



# Create donut chart

donut_chart <- ggplot(theft_type_2022, aes(ymax = ymax, ymin = ymin,
                                           
                                           xmax = 4, xmin = 2.5, fill = type)) +
  
  geom_rect(color = "white", size = 1.5) +
  
  geom_text(aes(x = 3.25, y = label_position,
                
                label = paste0(format(count, big.mark = ","), "\n",
                               
                               round(percentage, 1), "%")),
            
            color = "white", fontface = "bold", size = 5) +
  
  coord_polar(theta = "y") +
  
  xlim(c(1, 4)) +
  
  scale_fill_manual(values = c("#D32F2F", "#1976D2")) +
  
  theme_minimal() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    legend.position = "bottom",
    
    legend.title = element_blank(),
    
    legend.text = element_text(size = 12),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Vehicle Theft Composition in 2022",
    
    subtitle = "Kia/Hyundai vehicles represent over 1/3 of all vehicle thefts"
    
  )



ggsave("2_donut_chart_theft_type.png", donut_chart, width = 10, height = 8, dpi = 300)

print(donut_chart)



# ==============================================================================

# VISUALIZATION 3: STACKED BAR CHART - Yearly Theft Composition

# ==============================================================================



# Prepare data for stacked bar

yearly_stacked <- kia_hyundai_thefts %>%
  
  group_by(year) %>%
  
  summarise(
    
    `Kia/Hyundai Thefts` = sum(countKiaHyundaiThefts, na.rm = TRUE),
    
    `Other Vehicle Thefts` = sum(countOtherThefts, na.rm = TRUE)
    
  ) %>%
  
  pivot_longer(cols = c(`Kia/Hyundai Thefts`, `Other Vehicle Thefts`),
               
               names_to = "theft_type",
               
               values_to = "count")



# Create stacked bar chart

stacked_bar <- ggplot(yearly_stacked, aes(x = factor(year), y = count, fill = theft_type)) +
  
  geom_bar(stat = "identity", color = "white", size = 0.8) +
  
  geom_text(aes(label = format(count, big.mark = ",")),
            
            position = position_stack(vjust = 0.5),
            
            color = "white", fontface = "bold", size = 4) +
  
  scale_fill_manual(values = c("#E53935", "#43A047")) +
  
  scale_y_continuous(labels = comma, expand = c(0, 0)) +
  
  theme_minimal() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    axis.title = element_text(size = 12, face = "bold"),
    
    axis.text = element_text(size = 11),
    
    legend.position = "bottom",
    
    legend.title = element_blank(),
    
    legend.text = element_text(size = 11),
    
    panel.grid.major.x = element_blank(),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Annual Vehicle Theft Trends (2019-2022)",
    
    subtitle = "Kia/Hyundai thefts surged dramatically while overall thefts remained stable",
    
    x = "Year",
    
    y = "Number of Thefts"
    
  )



ggsave("3_stacked_bar_yearly.png", stacked_bar, width = 12, height = 7, dpi = 300)

print(stacked_bar)



# ==============================================================================

# VISUALIZATION 4: TREE MAP - Total Thefts by City

# ==============================================================================



# Prepare data for tree map (all cities)

treemap_data <- city_totals %>%
  
  mutate(
    
    city_state = paste(city, state, sep = ", "),
    
    label = paste0(city, "\n", format(total_kia_hyundai, big.mark = ","))
    
  )



# Create tree map

tree_map <- ggplot(treemap_data, aes(area = total_kia_hyundai, fill = total_kia_hyundai,
                                     
                                     label = label)) +
  
  geom_treemap(color = "white", size = 2) +
  
  geom_treemap_text(color = "white", place = "centre",
                    
                    fontface = "bold", size = 12, grow = FALSE) +
  
  scale_fill_gradient(low = "#FFF59D", high = "#C62828",
                      
                      labels = comma, name = "Total Thefts") +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    legend.position = "right",
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Geographic Distribution of Kia/Hyundai Thefts (2019-2022)",
    
    subtitle = "Size represents total thefts per city - Chicago dominates the crisis"
    
  )



ggsave("4_treemap_cities.png", tree_map, width = 14, height = 9, dpi = 300)

print(tree_map)



# ==============================================================================

# VISUALIZATION 5: STACKED AREA CHART - Monthly Theft Trends Over Time

# ==============================================================================



# Prepare data for stacked area chart

area_data <- monthly_aggregate %>%
  
  pivot_longer(cols = c(kia_hyundai_thefts, other_thefts),
               
               names_to = "theft_type",
               
               values_to = "count") %>%
  
  mutate(theft_type = recode(theft_type,
                             
                             "kia_hyundai_thefts" = "Kia/Hyundai",
                             
                             "other_thefts" = "Other Vehicles"))



# Create stacked area chart

stacked_area <- ggplot(area_data, aes(x = date, y = count, fill = theft_type)) +
  
  geom_area(alpha = 0.8, position = "stack") +
  
  scale_fill_manual(values = c("Kia/Hyundai" = "#D32F2F",
                               
                               "Other Vehicles" = "#1976D2")) +
  
  scale_x_date(date_breaks = "6 months", date_labels = "%b %Y") +
  
  scale_y_continuous(labels = comma, expand = c(0, 0)) +
  
  theme_minimal() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    axis.title = element_text(size = 12, face = "bold"),
    
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    
    axis.text.y = element_text(size = 11),
    
    legend.position = "bottom",
    
    legend.title = element_blank(),
    
    legend.text = element_text(size = 11),
    
    panel.grid.minor = element_blank(),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Monthly Vehicle Theft Trends Across All Cities (2019-2022)",
    
    subtitle = "The Kia/Hyundai theft epidemic accelerated dramatically in late 2020",
    
    x = "Date",
    
    y = "Total Monthly Thefts"
    
  )



ggsave("5_stacked_area_monthly.png", stacked_area, width = 14, height = 7, dpi = 300)

print(stacked_area)



# ==============================================================================

# VISUALIZATION 6: AREA CHART - Milwaukee Case Study (Percentage Trend)

# ==============================================================================



# Create area chart showing percentage of Kia/Hyundai thefts in Milwaukee

milwaukee_area <- ggplot(milwaukee_data, aes(x = date, y = percentKiaHyundai * 100)) +
  
  geom_area(fill = "#E53935", alpha = 0.7) +
  
  geom_line(color = "#B71C1C", size = 1.2) +
  
  geom_hline(yintercept = 50, linetype = "dashed", color = "#424242", size = 1) +
  
  annotate("text", x = as.Date("2021-06-01"), y = 55,
           
           label = "Majority Threshold (50%)",
           
           color = "#424242", fontface = "bold", size = 4) +
  
  scale_x_date(date_breaks = "6 months", date_labels = "%b %Y") +
  
  scale_y_continuous(labels = function(x) paste0(x, "%"),
                     
                     breaks = seq(0, 80, 10),
                     
                     expand = c(0, 0),
                     
                     limits = c(0, 80)) +
  
  theme_minimal() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    axis.title = element_text(size = 12, face = "bold"),
    
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    
    axis.text.y = element_text(size = 11),
    
    panel.grid.minor = element_blank(),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Milwaukee: Kia/Hyundai Vehicles as Percentage of All Thefts",
    
    subtitle = "From 9% in 2019 to over 70% in 2021 - a devastating trend",
    
    x = "Date",
    
    y = "Percentage of All Vehicle Thefts"
    
  )



ggsave("6_area_milwaukee_percentage.png", milwaukee_area, width = 14, height = 7, dpi = 300)

print(milwaukee_area)



# ==============================================================================

# VISUALIZATION 7: LINE CHART - Top Cities Comparison (Bonus Visual)

# ==============================================================================



# Get top 6 cities

top6_cities <- city_totals %>%
  
  top_n(6, total_kia_hyundai) %>%
  
  pull(city)



# Filter data for top cities

top_cities_monthly <- kia_hyundai_thefts %>%
  
  filter(city %in% top6_cities) %>%
  
  mutate(city_state = paste(city, state, sep = ", "))



# Create line chart

line_chart <- ggplot(top_cities_monthly,
                     
                     aes(x = date, y = countKiaHyundaiThefts, color = city_state)) +
  
  geom_line(size = 1.2, alpha = 0.8) +
  
  geom_point(size = 2, alpha = 0.6) +
  
  scale_color_brewer(palette = "Dark2") +
  
  scale_x_date(date_breaks = "6 months", date_labels = "%b %Y") +
  
  scale_y_continuous(labels = comma) +
  
  theme_minimal() +
  
  theme(
    
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    
    axis.title = element_text(size = 12, face = "bold"),
    
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    
    axis.text.y = element_text(size = 11),
    
    legend.position = "bottom",
    
    legend.title = element_blank(),
    
    legend.text = element_text(size = 10),
    
    panel.grid.minor = element_blank(),
    
    plot.margin = margin(20, 20, 20, 20)
    
  ) +
  
  labs(
    
    title = "Monthly Kia/Hyundai Theft Trends in Most Affected Cities",
    
    subtitle = "Chicago experienced an unprecedented surge beginning mid-2022",
    
    x = "Date",
    
    y = "Monthly Kia/Hyundai Thefts"
    
  )



ggsave("7_line_top_cities.png", line_chart, width = 14, height = 8, dpi = 300)

print(line_chart)



# ==============================================================================

# VISUALIZATION 8: BAR CHART - National Impact 2019 vs 2022 (Bonus Visual)

# ==============================================================================



# Calculate percentage change by city

city_change <- kia_hyundai_thefts %>%
  
  filter(year %in% c(2019, 2022)) %>%
  
  group_by(city, state, year) %>%
  
  summarise(total = sum(countKiaHyundaiThefts, na.rm = TRUE)) %>%
  
  pivot_wider(names_from = year, values_from = total, names_prefix = "year_") %>%
  
  mutate(
    
    percent_change = ((year_2022 - year_2019) / year_2019) * 100,
    
    city_state = paste(city, state, sep = ", ")
    
  ) %>%
  
  filter(!is.infinite(percent_change)) %>%
  
  arrange(desc(percent_change)) %>%
  
  top_n(10, percent_change)



# Create bar chart

change_bar <- ggplot(city_change, aes(x = reorder(city_state, percent_change),
                                      y = percent_change, fill = percent_change)) +
  geom_bar(stat = "identity", color = "white", size = 0.5) +
  geom_text(aes(label = paste0("+", round(percent_change, 0), "%")),
            hjust = -0.2, fontface = "bold", size = 4) +
  scale_fill_gradient(low = "#FF6F00", high = "#B71C1C") +
  coord_flip() +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5, size = 11, margin = margin(b = 15)),
    axis.title = element_text(size = 12, face = "bold"),
    axis.text = element_text(size = 11),
    legend.position = "none",
    panel.grid.major.y = element_blank(),
    plot.margin = margin(20, 40, 20, 20)
  ) +
  labs(
    title = "Cities with Highest Kia/Hyundai Theft Increase (2019-2022)",
    subtitle = "Some cities saw increases of over 5,000%",
    x = "",
    y = "Percentage Increase (%)"
  )

ggsave("8_bar_percent_change.png", change_bar, width = 12, height = 9, dpi = 300)

print(change_bar)

# ==============================================================================
# SUMMARY STATISTICS FOR REPORT
# ==============================================================================

# Calculate key statistics

total_kia_hyundai_2019 <- sum(kia_hyundai_thefts$countKiaHyundaiThefts[kia_hyundai_thefts$year == 2019], na.rm = TRUE)

total_kia_hyundai_2022 <- sum(kia_hyundai_thefts$countKiaHyundaiThefts[kia_hyundai_thefts$year == 2022], na.rm = TRUE)

percent_increase <- ((total_kia_hyundai_2022 - total_kia_hyundai_2019) / total_kia_hyundai_2019) * 100

cat("\n==============================================================================\n")
cat("KEY STATISTICS FOR REPORT\n")
cat("==============================================================================\n")

cat("Total Kia/Hyundai Thefts 2019:", format(total_kia_hyundai_2019, big.mark = ","), "\n")

cat("Total Kia/Hyundai Thefts 2022:", format(total_kia_hyundai_2022, big.mark = ","), "\n")

cat("Overall Increase:", round(percent_increase, 1), "%\n")

cat("Cities Analyzed:", length(unique(kia_hyundai_thefts$city)), "\n")

cat("Most Affected City:", city_totals$city[1], ",", city_totals$state[1], "\n")

cat("Thefts in Most Affected City:", format(city_totals$total_kia_hyundai[1], big.mark = ","), "\n")

cat("==============================================================================\n")

print("Analysis complete! All visualizations have been saved.")
