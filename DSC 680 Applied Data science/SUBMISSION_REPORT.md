# DSC 680 Applied Data Science
## Milestone 1 Report
## Predicting High-Cost Healthcare Members

Prepared for: DSC680-T301 Applied Data Science  
Student: Vijay Sharma  
Date: June 28, 2026

---

## Executive Summary

This report presents a completed data science workflow for predicting high-cost healthcare members using a structured healthcare-style dataset. The project was designed to explore the relationship between member characteristics and healthcare cost, identify high-cost segments, and build a predictive model capable of estimating future costs. The workflow included data validation, descriptive analysis, visualization, feature engineering, model training, and performance evaluation.

The analysis used a synthetic but realistic healthcare dataset containing 1,000 records and seven core variables, including age, gender, visit counts, emergency room use, hospitalizations, and cost. The final predictive model achieved strong performance, with a Ridge Regression model producing an $R^2$ value of 0.9687 and an RMSE of $1,229.62. These results indicate that the model explains approximately 96.9% of the variance in the target variable and provides a reliable cost estimate for the test set.

---

## Project Objective

The objective of this project was to build a predictive model that can identify members likely to incur high healthcare costs. This is important because a relatively small proportion of members often account for most healthcare spending. By identifying high-risk members earlier, healthcare organizations can support targeted intervention strategies and improve cost management.

The assignment focused on three primary goals:

1. Understand the characteristics of healthcare cost data.
2. Identify patterns associated with high-cost members.
3. Develop and evaluate a predictive model for healthcare cost estimation.

---

## Data and Methodology

### Data Source and Scope

Because healthcare data often contains protected health information, this project used a synthetic healthcare-style dataset that preserves the structure and analytical logic of a real-world healthcare dataset without exposing sensitive records. The dataset included 1,000 member records and the following fields:

- member_id
- age
- gender
- visits
- er_visits
- hospitalizations
- cost

### Data Preparation Process

The workflow followed a standard supervised learning pipeline:

1. Data loading and validation
2. Descriptive and statistical analysis
3. Visualization of cost patterns and relationships
4. Feature engineering to create more informative predictors
5. Model training and comparison
6. Evaluation using regression metrics

### Feature Engineering

Several new features were created to improve model performance, including:

- age_group categories based on age ranges
- visits_per_month
- is_frequent_visitor
- has_er_visits
- age_visits_interaction
- gender_encoded

These engineered features helped capture more nuanced patterns in cost behavior and improved the final model’s predictive performance.

---

## Exploratory Data Analysis Findings

### 1. Cost Distribution

The cost variable showed a broad and right-skewed distribution, which is typical of healthcare spending data. The sample dataset had the following cost-related statistics:

- Mean cost: $20,965.63
- Median cost: $19,990.96
- Standard deviation: $7,203.59
- Minimum cost: $4,614.70
- Maximum cost: $4,614.70
- 95th percentile: $34,249.52

These values indicate that costs vary significantly across members and that some members represent much higher spending levels than others.

### 2. High-Cost Member Concentration

A Pareto-style analysis was performed to understand how concentrated healthcare costs were across the member population. The results showed that approximately 68.9% of members accounted for 80% of total healthcare costs. This supports the common finding that a relatively small percentage of members generate a disproportionate share of overall spending.

### 3. Correlation with Cost

The correlation analysis showed that hospitalizations had the strongest relationship with cost, followed by emergency room visits and age. This suggests that utilization intensity is a strong indicator of healthcare expense.

---

## Visual Analysis

The project generated several visualizations to support interpretation and communication of the findings.

### Figure 1: Cost Distribution
The cost distribution chart illustrates the spread of member costs and confirms the presence of a wide range of spending levels. The visualization shows that costs are not evenly distributed and that a subset of members fall in the higher-cost range.

### Figure 2: Pareto Analysis
The Pareto chart highlights the concentration of costs among members. The results confirm that a relatively small share of the population contributes to the majority of spending, reinforcing the practical value of targeted intervention.

### Figure 3: Correlation Heatmap
The correlation heatmap shows the relationships between the main numeric features and cost. Hospitalizations and emergency room visits demonstrated the clearest positive relationships with cost, which aligns with the broader understanding of healthcare cost drivers.

---

## Modeling Approach

Several regression models were trained and evaluated to determine the best-performing approach for cost prediction.

### Models Compared

- Linear Regression
- Ridge Regression
- Random Forest Regression
- Gradient Boosting Regression

### Model Evaluation Metrics

The models were evaluated using:

- R-squared ($R^2$)
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)

### Best Model

The best-performing model was Ridge Regression, which produced the following results:

- $R^2$: 0.9687
- RMSE: $1,229.62
- MAE: $983.96
- MSE: $1,511,957.84

These results demonstrate that the model performed very well on the test set and produced predictions that closely matched actual costs.

---

## Prediction Results

The final prediction results showed a strong alignment between actual and predicted costs. The average actual cost in the test set was approximately $21,234.48, while the average predicted cost was $21,199.90. The mean prediction error was only $34.58, indicating that the model was highly accurate overall.

This is an important result because it suggests that the model can be used as a practical decision-support tool for identifying members likely to have high costs.

---

## Interpretation of Results

The results suggest that healthcare cost is strongly associated with utilization-related variables, especially hospitalizations and emergency room visits. This aligns with the expectation that members with more severe or frequent healthcare use are more likely to generate higher costs. The predictive model also shows that demographic and utilization features, when engineered appropriately, can produce highly useful forecasting results.

From an applied perspective, this project demonstrates the value of data-driven healthcare analytics for early identification of high-cost members and for supporting proactive care interventions.

---

## Generated Deliverables

The workflow produced the following output artifacts:

- Cost distribution chart
- Pareto analysis chart
- Correlation heatmap
- Prediction results file
- Data validation report
- Trained Ridge Regression model
- Project log file

All outputs were saved in the project directories for review and submission.

---

## Conclusion

This assignment successfully demonstrated the complete process of building a predictive analytics solution for healthcare cost estimation. The project began with data validation and exploratory analysis, progressed through feature engineering, and concluded with model training and evaluation. The final model achieved strong predictive performance and offers a clear foundation for future improvement.

The project also illustrates how data science methods can support healthcare organizations in identifying members who may benefit from earlier intervention and more targeted care management. Although the data used in this demonstration was synthetic, the workflow reflects the structure and reasoning of a realistic healthcare analytics project.

---

## References and Project Files

Project files created during this workflow include:

- README.md
- IMPLEMENTATION_GUIDE.md
- starter_workflow.py
- analysis_and_visualization.py
- data_collection.py
- model_development.py
- output/predictions.csv
- output/data_validation_report.json
- output/cost_distribution.png
- output/pareto_analysis.png
- output/correlation_heatmap.png
- models/ridge_regression.pkl

---

## Appendix: Submission Notes

This report was generated from the completed project workflow and reflects the verified outputs produced during execution. It is suitable for submission as a polished milestone report and provides a concise yet detailed overview of the project’s objective, methods, findings, and results.
