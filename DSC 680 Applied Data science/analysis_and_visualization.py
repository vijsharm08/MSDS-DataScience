"""
DSC680-T301 Applied Data Science
Analysis and Visualization Module

Handles data exploration, visualization, and preliminary analysis
for the high-cost healthcare member prediction project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class DataExplorer:
    """
    Comprehensive exploratory data analysis for healthcare datasets.
    """
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with DataFrame."""
        self.df = df
        self.insights = {}
    
    def generate_overview(self) -> str:
        """Generate high-level data overview."""
        overview = f"""
        ╔═══════════════════════════════════════╗
        ║     DATASET OVERVIEW                  ║
        ╠═══════════════════════════════════════╣
        ║ Shape:           {self.df.shape}                   ║
        ║ Columns:         {len(self.df.columns)}                          ║
        ║ Memory Usage:    {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB                ║
        ║ Duplicates:      {self.df.duplicated().sum()}                          ║
        ║ Missing Values:  {self.df.isnull().sum().sum()}                          ║
        ╚═══════════════════════════════════════╝
        
        Column Information:
        {self.df.dtypes}
        """
        return overview
    
    def analyze_numeric_columns(self) -> pd.DataFrame:
        """Analyze numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        analysis = pd.DataFrame({
            'Column': numeric_cols,
            'Count': self.df[numeric_cols].count(),
            'Mean': self.df[numeric_cols].mean(),
            'Std': self.df[numeric_cols].std(),
            'Min': self.df[numeric_cols].min(),
            'Max': self.df[numeric_cols].max(),
            'Q1': self.df[numeric_cols].quantile(0.25),
            'Median': self.df[numeric_cols].quantile(0.50),
            'Q3': self.df[numeric_cols].quantile(0.75)
        })
        
        return analysis.T
    
    def analyze_categorical_columns(self) -> Dict:
        """Analyze categorical columns."""
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        analysis = {}
        for col in categorical_cols:
            analysis[col] = {
                'unique_values': self.df[col].nunique(),
                'top_values': self.df[col].value_counts().head(5).to_dict(),
                'missing': self.df[col].isnull().sum()
            }
        
        return analysis
    
    def detect_outliers(self, column: str, method: str = 'iqr') -> pd.DataFrame:
        """
        Detect outliers in a column.
        
        Args:
            column: Column name
            method: 'iqr' or 'zscore'
        
        Returns:
            DataFrame with outlier information
        """
        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(self.df[column].dropna()))
            outliers = self.df[np.abs(stats.zscore(self.df[column])) > 3]
        
        logger.info(f"Detected {len(outliers)} outliers in '{column}'")
        return outliers
    
    def correlation_analysis(self, numeric_only: bool = True) -> pd.DataFrame:
        """Calculate correlation matrix."""
        if numeric_only:
            return self.df.select_dtypes(include=[np.number]).corr()
        else:
            return self.df.corr()


class HealthcareVisualizer:
    """
    Create visualizations for healthcare cost analysis.
    """
    
    @staticmethod
    def plot_cost_distribution(costs: pd.Series, title: str = "Healthcare Cost Distribution"):
        """Plot cost distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(costs, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0].set_title(f"{title} - Histogram")
        axes[0].set_xlabel("Cost ($)")
        axes[0].set_ylabel("Frequency")
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(costs, vert=True)
        axes[1].set_title(f"{title} - Box Plot")
        axes[1].set_ylabel("Cost ($)")
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_pareto_analysis(costs: pd.Series, title: str = "Pareto Analysis"):
        """Create Pareto chart for cost concentration."""
        sorted_costs = costs.sort_values(ascending=False).reset_index(drop=True)
        cumsum = sorted_costs.cumsum()
        cumsum_pct = (cumsum / cumsum.iloc[-1]) * 100
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Bar chart for individual costs
        ax1.bar(range(len(sorted_costs)), sorted_costs, alpha=0.6, color='steelblue')
        ax1.set_xlabel("Member (sorted by cost)")
        ax1.set_ylabel("Cost ($)")
        ax1.set_title(title)
        
        # Line chart for cumulative percentage
        ax2 = ax1.twinx()
        ax2.plot(range(len(cumsum_pct)), cumsum_pct, color='red', marker='o', linewidth=2)
        ax2.set_ylabel("Cumulative Percentage (%)")
        ax2.axhline(y=80, color='green', linestyle='--', label='80% Threshold')
        ax2.legend()
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_cost_by_category(df: pd.DataFrame, category_col: str, cost_col: str):
        """Plot cost distribution by category."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        df.boxplot(column=cost_col, by=category_col, ax=ax)
        ax.set_title(f"Cost Distribution by {category_col}")
        ax.set_xlabel(category_col)
        ax.set_ylabel("Cost ($)")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_correlation_heatmap(correlation_matrix: pd.DataFrame):
        """Plot correlation heatmap."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title("Feature Correlation Matrix")
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_cost_trend(df: pd.DataFrame, date_col: str, cost_col: str):
        """Plot cost trend over time."""
        df_sorted = df.sort_values(date_col)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(df_sorted[date_col], df_sorted[cost_col].cumsum(), marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Cost ($)")
        ax.set_title("Healthcare Cost Trend Over Time")
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class StatisticalAnalyzer:
    """
    Perform statistical analyses on healthcare data.
    """
    
    @staticmethod
    def hypothesis_test_ttest(group1: pd.Series, group2: pd.Series) -> Tuple[float, float]:
        """
        Perform t-test between two groups.
        
        Returns:
            Tuple of (t-statistic, p-value)
        """
        from scipy import stats
        t_stat, p_value = stats.ttest_ind(group1, group2)
        return t_stat, p_value
    
    @staticmethod
    def hypothesis_test_anova(*groups) -> Tuple[float, float]:
        """
        Perform ANOVA test across multiple groups.
        
        Returns:
            Tuple of (F-statistic, p-value)
        """
        from scipy import stats
        f_stat, p_value = stats.f_oneway(*groups)
        return f_stat, p_value
    
    @staticmethod
    def chi_square_test(contingency_table: pd.DataFrame) -> Tuple[float, float]:
        """
        Perform chi-square test for independence.
        
        Returns:
            Tuple of (chi-square statistic, p-value)
        """
        from scipy.stats import chi2_contingency
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        return chi2, p_value


class ReportGenerator:
    """
    Generate comprehensive analysis reports.
    """
    
    @staticmethod
    def generate_summary_report(explorer: DataExplorer) -> str:
        """Generate summary report."""
        report = explorer.generate_overview()
        report += f"\n\nNumeric Columns Analysis:\n{explorer.analyze_numeric_columns()}"
        report += f"\n\nCategorical Columns Analysis:\n{explorer.analyze_categorical_columns()}"
        return report
    
    @staticmethod
    def save_report_to_file(content: str, filepath: str):
        """Save report to file."""
        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Report saved to: {filepath}")


if __name__ == "__main__":
    print("Healthcare Data Analysis and Visualization Module")
    print("Ready for use with high-cost member prediction project")
