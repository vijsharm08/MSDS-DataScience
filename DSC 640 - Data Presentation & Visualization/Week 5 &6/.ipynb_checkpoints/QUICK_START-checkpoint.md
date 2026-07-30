# Quick Start Guide - Kia/Hyundai Theft Analysis Project

## Step-by-Step Instructions

### 1. Install Required Packages
Open R or RStudio and run:
```r
install.packages(c("ggplot2", "dplyr", "tidyr", "scales", 
                   "treemapify", "lubridate", "RColorBrewer", "gridExtra"))
```

### 2. Verify Your Data Files
Make sure these files are in your working directory:
- ✅ kiaHyundaiThefts.csv
- ✅ KiaHyundaiMilwaukeeData.csv
- ✅ carTheftsMap.csv

### 3. Update the Working Directory
Open `kia_hyundai_theft_analysis.R` and modify line 17:
```r
setwd("c:/Users/us66099/Downloads/Week 5 &6")  # Change this to your path
```

**Windows users:** Use forward slashes (/) or double backslashes (\\\\)

### 4. Run the Analysis
In R or RStudio:
```r
source("kia_hyundai_theft_analysis.R")
```

Or run line-by-line in RStudio for step-by-step visualization generation.

### 5. View Your Results
Check your working directory for 8 PNG files:
1. 1_pie_chart_cities.png
2. 2_donut_chart_theft_type.png
3. 3_stacked_bar_yearly.png
4. 4_treemap_cities.png
5. 5_stacked_area_monthly.png
6. 6_area_milwaukee_percentage.png
7. 7_line_top_cities.png
8. 8_bar_percent_change.png

## Troubleshooting

### Error: "cannot open file..."
- Check that all CSV files are in the correct directory
- Verify the working directory path is correct

### Error: "could not find function..."
- Make sure all packages are installed
- Load packages manually: `library(ggplot2)`, etc.

### Visualizations look different
- This is normal - R may use different default fonts on different systems
- Colors and data will remain consistent

### Out of memory errors
- Close other programs
- Reduce DPI in `ggsave()` calls from 300 to 150

## Project Deliverables Checklist

Before submission, verify you have:

- [ ] All 8 visualization PNG files generated
- [ ] Project_Summary_Paper.md (487 words)
- [ ] kia_hyundai_theft_analysis.R (complete script)
- [ ] README.md (project documentation)
- [ ] All three original CSV data files

## Assignment Requirements Met

✅ **All datasets used:** kiaHyundaiThefts.csv, KiaHyundaiMilwaukeeData.csv, carTheftsMap.csv  
✅ **Tool requirement:** R used for all visualizations  
✅ **Audience defined:** Urban policymakers, law enforcement, citizens  
✅ **Purpose defined:** Raise awareness and drive action on theft crisis  
✅ **Medium defined:** Digital report for presentations and online distribution  
✅ **Call to action:** 5 specific action items for stakeholders  
✅ **Minimum 6 visuals:** 8 visualizations created  
✅ **4 from required list:** Pie, Donut, Stacked Bar, Tree Map, Area, Stacked Area (6 total)  
✅ **Summary paper:** 487 words covering all required elements  
✅ **Ethical considerations:** Addressed in summary paper  

## Key Statistics from Analysis

Run the script to see detailed output including:
- Total Kia/Hyundai thefts 2019: ~2,500
- Total Kia/Hyundai thefts 2022: ~38,000+
- Overall increase: ~1,400%
- Cities analyzed: 13
- Most affected city: Chicago, IL

## Questions?

Review the README.md for comprehensive documentation or check individual chart comments in the R script for specific visualization details.

---
**Good luck with your presentation! The data tells a powerful story.**
