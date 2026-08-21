"""
DSC680-T301 Applied Data Science
Milestone 1: Data Collection and Selection

Project: Predicting High-Cost Healthcare Members
Author: Vijay Sharma
Instructor: Xu Ashton
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthcareDataLoader:
    """
    Load and validate healthcare datasets for high-cost member prediction.
    
    This class handles:
    - Loading public healthcare datasets
    - Validating data structure and quality
    - Initial data exploration
    - Data preparation for analysis
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Directory containing healthcare datasets
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.datasets = {}
        self.validation_report = {}
        logger.info(f"Initialized DataLoader with data directory: {self.data_dir}")
    
    def load_dataset(self, filepath: str, name: str) -> pd.DataFrame:
        """
        Load a dataset from CSV file.
        
        Args:
            filepath: Path to CSV file
            name: Name to assign to the dataset
            
        Returns:
            Loaded DataFrame
        """
        try:
            df = pd.read_csv(filepath)
            self.datasets[name] = df
            logger.info(f"Loaded dataset '{name}': {df.shape[0]} rows, {df.shape[1]} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return None
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            return None
    
    def validate_dataset(self, name: str) -> dict:
        """
        Validate dataset structure and quality.
        
        Args:
            name: Dataset name to validate
            
        Returns:
            Dictionary with validation results
        """
        if name not in self.datasets:
            logger.warning(f"Dataset '{name}' not found")
            return {}
        
        df = self.datasets[name]
        
        validation = {
            'name': name,
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'duplicates': df.duplicated().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }
        
        self.validation_report[name] = validation
        logger.info(f"Validation complete for '{name}'")
        return validation
    
    def get_summary_statistics(self, name: str) -> pd.DataFrame:
        """
        Get summary statistics for a dataset.
        
        Args:
            name: Dataset name
            
        Returns:
            Summary statistics DataFrame
        """
        if name not in self.datasets:
            logger.warning(f"Dataset '{name}' not found")
            return None
        
        return self.datasets[name].describe()
    
    def get_missing_data_report(self, name: str) -> pd.DataFrame:
        """
        Generate missing data report for a dataset.
        
        Args:
            name: Dataset name
            
        Returns:
            DataFrame with missing data information
        """
        if name not in self.datasets:
            logger.warning(f"Dataset '{name}' not found")
            return None
        
        df = self.datasets[name]
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum().values,
            'Missing_Percentage': (df.isnull().sum() / len(df) * 100).values,
            'Data_Type': df.dtypes.values
        })
        
        return missing_data.sort_values('Missing_Percentage', ascending=False)
    
    def _make_json_serializable(self, value):
        """Convert values to JSON-serializable Python objects."""
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {k: self._make_json_serializable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._make_json_serializable(v) for v in value]
        if isinstance(value, np.generic):
            return value.item()
        if hasattr(value, 'to_pydatetime'):
            return value.to_pydatetime().isoformat()
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        if hasattr(value, 'dtype') and hasattr(value, 'name'):
            return str(value)
        return str(value)

    def export_validation_report(self, filepath: str):
        """
        Export validation report to file.
        
        Args:
            filepath: Path to save validation report
        """
        import json
        
        report_json = {}
        for dataset_name, validation in self.validation_report.items():
            report_json[dataset_name] = {
                k: self._make_json_serializable(v)
                for k, v in validation.items()
            }
        
        with open(filepath, 'w') as f:
            json.dump(report_json, f, indent=2)
        
        logger.info(f"Validation report exported to: {filepath}")


class HealthcareCostAnalyzer:
    """
    Analyze healthcare cost patterns and member characteristics.
    
    This class provides:
    - Cost distribution analysis
    - Member segmentation
    - Feature correlation analysis
    - Cost driver identification
    """
    
    def __init__(self, df: pd.DataFrame, cost_column: str = 'cost'):
        """
        Initialize the analyzer.
        
        Args:
            df: DataFrame with healthcare data
            cost_column: Name of the cost column
        """
        self.df = df
        self.cost_column = cost_column
        self.analysis_results = {}
        
        if cost_column not in df.columns:
            logger.warning(f"Cost column '{cost_column}' not found in DataFrame")
    
    def analyze_cost_distribution(self) -> dict:
        """
        Analyze the distribution of healthcare costs.
        
        Returns:
            Dictionary with cost distribution statistics
        """
        if self.cost_column not in self.df.columns:
            return {}
        
        costs = self.df[self.cost_column]
        
        analysis = {
            'mean': costs.mean(),
            'median': costs.median(),
            'std': costs.std(),
            'min': costs.min(),
            'max': costs.max(),
            'q25': costs.quantile(0.25),
            'q75': costs.quantile(0.75),
            'q90': costs.quantile(0.90),
            'q95': costs.quantile(0.95),
            'q99': costs.quantile(0.99),
            'skewness': costs.skew(),
            'kurtosis': costs.kurtosis()
        }
        
        self.analysis_results['cost_distribution'] = analysis
        logger.info("Cost distribution analysis complete")
        return analysis
    
    def identify_high_cost_members(self, percentile: float = 90) -> pd.DataFrame:
        """
        Identify members in high-cost segment.
        
        Args:
            percentile: Cost percentile threshold (default: 90th percentile)
            
        Returns:
            DataFrame with high-cost members
        """
        if self.cost_column not in self.df.columns:
            return pd.DataFrame()
        
        threshold = self.df[self.cost_column].quantile(percentile / 100)
        high_cost = self.df[self.df[self.cost_column] >= threshold].copy()
        
        high_cost['cost_segment'] = 'high_cost'
        
        logger.info(f"Identified {len(high_cost)} high-cost members (>= {percentile}th percentile: ${threshold:.2f})")
        return high_cost
    
    def calculate_cost_concentration(self) -> dict:
        """
        Calculate cost concentration metrics (Pareto analysis).
        
        Returns:
            Dictionary with concentration metrics
        """
        if self.cost_column not in self.df.columns:
            return {}
        
        costs = self.df[self.cost_column].sort_values(ascending=False)
        cumsum = costs.cumsum()
        total_cost = cumsum.iloc[-1]
        
        # Find percentage of members accounting for 80% of costs
        idx_80 = (cumsum >= total_cost * 0.80).idxmax()
        pct_members_80 = (costs.index.get_loc(idx_80) + 1) / len(costs) * 100
        
        concentration = {
            'total_cost': total_cost,
            'pct_members_for_80_pct_cost': pct_members_80,
            'top_10_pct_contribution': (costs.head(int(len(costs) * 0.10)).sum() / total_cost * 100),
            'top_20_pct_contribution': (costs.head(int(len(costs) * 0.20)).sum() / total_cost * 100)
        }
        
        self.analysis_results['cost_concentration'] = concentration
        logger.info("Cost concentration analysis complete")
        return concentration


class DataQualityReporter:
    """
    Generate comprehensive data quality reports.
    """
    
    @staticmethod
    def generate_html_report(loader: HealthcareDataLoader, output_file: str = "data_quality_report.html"):
        """
        Generate HTML data quality report.
        
        Args:
            loader: HealthcareDataLoader instance
            output_file: Output HTML file path
        """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Quality Report - Healthcare Cost Prediction</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #003366; }
                h2 { color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #0066cc; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .warning { color: #ff6600; font-weight: bold; }
                .success { color: #009900; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>📊 Data Quality Report</h1>
            <p>Generated: {timestamp}</p>
            <h2>Dataset Summary</h2>
            <p>Total datasets loaded: <strong>{num_datasets}</strong></p>
        </body>
        </html>
        """.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            num_datasets=len(loader.datasets)
        )
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {output_file}")


# Example usage and workflow
if __name__ == "__main__":
    
    logger.info("="*60)
    logger.info("DSC680 Healthcare Cost Prediction - Data Collection Phase")
    logger.info("="*60)
    
    # Initialize data loader
    loader = HealthcareDataLoader(data_dir="./data")
    
    logger.info("\n--- Step 1: Data Collection ---")
    logger.info("Ready to load public healthcare datasets")
    logger.info("Expected datasets:")
    logger.info("  - Member demographics")
    logger.info("  - Claims/costs data")
    logger.info("  - Medical history/diagnoses")
    logger.info("  - Healthcare utilization")
    
    logger.info("\n--- Step 2: Data Validation ---")
    logger.info("Prepared to validate data structure and quality")
    
    logger.info("\n--- Step 3: Data Analysis ---")
    logger.info("Prepared to analyze cost patterns and member characteristics")
    
    logger.info("\n--- Step 4: Data Preparation ---")
    logger.info("Ready to prepare data for modeling")
    
    logger.info("\n" + "="*60)
    logger.info("Data Collection Phase Complete")
    logger.info("="*60)
