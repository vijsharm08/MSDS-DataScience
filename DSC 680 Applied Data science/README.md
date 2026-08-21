# DSC680-T301 Applied Data Science - Milestone 1

## Project: Predicting High-Cost Healthcare Members

**Course:** DSC680-T301 Applied Data Science (2267-1)  
**Instructor:** Xu Ashton  
**Student:** Vijay Sharma  
**Milestone:** 1 - Data Collection and Selection  

---

## Executive Summary

This project aims to build a **predictive model that identifies members likely to incur high healthcare costs**, enabling proactive intervention by healthcare organizations. Healthcare organizations such as Premera face rising costs driven by a small percentage of members who account for a disproportionately high share of healthcare expenses.

---

## Problem Statement

Healthcare organizations face critical challenges:
- **Rising Healthcare Costs**: A small percentage of members account for a disproportionately high share of expenses
- **Cost Drivers**: High costs are often associated with:
  - Emergency room visits
  - Hospitalizations
  - Chronic disease management
  - Complex medical conditions

---

## Solution Approach

### Objective
Develop a **data-driven approach** that enables healthcare organizations to:
- **Proactively identify** high-cost members
- **Intervene early** with targeted care management
- **Reduce healthcare expenditures** through prevention and optimization
- **Improve member outcomes** through personalized care strategies

### Data Strategy
Due to the sensitive nature of Protected Health Information (PHI), this project uses:
- **Publicly available datasets** that approximate enterprise healthcare data
- Datasets comparable to those used by organizations like Premera
- Ethical and compliant approach to healthcare data analysis

---

## Key Features of the Model

### What Can Be Achieved Through This Project:

1. **Member Segmentation**
   - Identify high-cost members before they generate significant expenses
   - Categorize members by risk level
   - Enable targeted interventions for high-risk populations

2. **Cost Prediction**
   - Predict annual or quarterly healthcare costs for individual members
   - Estimate total organization spend based on member populations
   - Forecast budget requirements

3. **Intervention Planning**
   - Recommend preventive care programs
   - Prioritize care management resources
   - Design targeted wellness initiatives

4. **ROI Analysis**
   - Measure cost avoidance from interventions
   - Calculate intervention effectiveness
   - Optimize healthcare spending

5. **Clinical Insights**
   - Identify common diagnoses among high-cost members
   - Detect patterns in healthcare utilization
   - Highlight areas for clinical improvement

6. **Organizational Benefits**
   - Reduce overall healthcare expenditures
   - Improve member satisfaction through proactive care
   - Enhance operational efficiency
   - Support evidence-based decision-making

---

## Data Sources

### Public Datasets Used
- Healthcare claims data approximating enterprise data structures
- Member demographic information
- Medical history and diagnosis codes
- Healthcare utilization patterns

### Data Characteristics
- Approximate structure of real enterprise healthcare data
- HIPAA-compliant and publicly available
- Sufficient volume for machine learning model development

---

## Methodology

### Phase 1: Data Collection and Selection (Current - Milestone 1)
- Identify and source appropriate public healthcare datasets
- Validate data structure and completeness
- Assess data quality and relevance
- Prepare datasets for analysis

### Phase 2: Exploratory Data Analysis (EDA)
- Analyze feature distributions
- Identify correlations and patterns
- Detect outliers and anomalies
- Understand cost drivers

### Phase 3: Feature Engineering
- Create derived features for predictive modeling
- Normalize and transform variables
- Handle missing values
- Prepare final feature set

### Phase 4: Model Development
- Build multiple predictive models
- Compare model performance
- Optimize hyperparameters
- Validate model accuracy

### Phase 5: Implementation and Deployment
- Create production-ready solution
- Develop visualization dashboards
- Document recommendations
- Plan for ongoing monitoring

---

## Expected Outcomes

### Deliverables
1. **Predictive Model**: High-accuracy model for cost prediction
2. **Member Risk Scores**: Individual risk assessments for members
3. **Analytics Dashboard**: Visual insights into cost patterns
4. **Recommendations**: Actionable interventions for high-cost members
5. **ROI Analysis**: Cost-benefit analysis of proposed interventions

### Performance Metrics
- Prediction accuracy (RMSE, MAE)
- Model precision and recall
- Area Under ROC Curve (AUC)
- Cost savings estimation

---

## Technical Stack

- **Programming Languages**: Python
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Statistical Analysis**: SciPy, Statsmodels
- **Notebooks**: Jupyter

---

## References

Fregly, C., Barth, A., & Eigenbrode, S. (2023). *Generative AI on AWS*. O'Reilly Media.

---

## Project Timeline

| Milestone | Task | Status |
|-----------|------|--------|
| M1 | Data Collection and Selection | ✅ In Progress |
| M2 | Exploratory Data Analysis | ⏳ Pending |
| M3 | Feature Engineering | ⏳ Pending |
| M4 | Model Development | ⏳ Pending |
| M5 | Deployment & Documentation | ⏳ Pending |

---

## Notes

- This project follows ethical AI principles by using public data
- HIPAA compliance is maintained through use of non-sensitive public datasets
- Results are generalizable to healthcare organizations of any size
- Model can be adapted for different healthcare systems and populations

---

*Last Updated: June 28, 2026*
