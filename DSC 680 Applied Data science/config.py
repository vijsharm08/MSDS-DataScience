"""
Configuration module for DSC680 Healthcare Cost Prediction Project
"""

from pathlib import Path
from typing import Dict

# Project Structure
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, MODELS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


class ProjectConfig:
    """Configuration settings for the project."""
    
    # Project metadata
    PROJECT_NAME = "High-Cost Healthcare Member Prediction"
    PROJECT_CODE = "DSC680-T301"
    COURSE = "Applied Data Science"
    INSTRUCTOR = "Xu Ashton"
    AUTHOR = "Vijay Sharma"
    VERSION = "1.0.0"
    
    # Data configuration
    DATA_RANDOM_STATE = 42
    TEST_SIZE = 0.2
    VALIDATION_SIZE = 0.1
    
    # Model configuration
    MODEL_CONFIGS = {
        'linear_regression': {
            'name': 'Linear Regression',
            'params': {}
        },
        'ridge_regression': {
            'name': 'Ridge Regression',
            'params': {'alpha': 1.0}
        },
        'lasso_regression': {
            'name': 'Lasso Regression',
            'params': {'alpha': 0.1}
        },
        'random_forest': {
            'name': 'Random Forest',
            'params': {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 2,
                'random_state': 42
            }
        },
        'gradient_boosting': {
            'name': 'Gradient Boosting',
            'params': {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 5,
                'random_state': 42
            }
        }
    }
    
    # Feature configuration
    FEATURE_GROUPS = {
        'demographic': ['age', 'gender', 'location'],
        'utilization': ['visits', 'er_visits', 'hospitalizations'],
        'clinical': ['diagnoses', 'medications', 'procedures'],
        'financial': ['cost', 'insurance_type', 'deductible']
    }
    
    # Cost thresholds (percentiles for high-cost segmentation)
    COST_PERCENTILES = {
        'high_cost': 90,      # Top 10% of costs
        'very_high_cost': 95, # Top 5% of costs
        'extreme_cost': 99    # Top 1% of costs
    }
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = OUTPUT_DIR / 'project.log'
    
    # Output configuration
    SAVE_FIGURES = True
    FIGURE_FORMAT = 'png'
    FIGURE_DPI = 300
    FIGURE_STYLE = 'seaborn-v0_8-whitegrid'
    
    # Performance metrics
    EVALUATION_METRICS = [
        'mse',      # Mean Squared Error
        'mae',      # Mean Absolute Error
        'rmse',     # Root Mean Squared Error
        'r2_score', # R² Score
        'mape'      # Mean Absolute Percentage Error
    ]
    
    @classmethod
    def get_data_path(cls, filename: str) -> Path:
        """Get path to data file."""
        return DATA_DIR / filename
    
    @classmethod
    def get_output_path(cls, filename: str) -> Path:
        """Get path to output file."""
        return OUTPUT_DIR / filename
    
    @classmethod
    def get_model_path(cls, model_name: str) -> Path:
        """Get path to model file."""
        return MODELS_DIR / f"{model_name}.pkl"
    
    @classmethod
    def get_report_path(cls, report_name: str) -> Path:
        """Get path to report file."""
        return REPORTS_DIR / f"{report_name}.html"
    
    @classmethod
    def to_dict(cls) -> Dict:
        """Convert configuration to dictionary."""
        return {
            'project_name': cls.PROJECT_NAME,
            'project_code': cls.PROJECT_CODE,
            'course': cls.COURSE,
            'instructor': cls.INSTRUCTOR,
            'author': cls.AUTHOR,
            'version': cls.VERSION,
            'test_size': cls.TEST_SIZE,
            'model_configs': cls.MODEL_CONFIGS,
            'cost_percentiles': cls.COST_PERCENTILES
        }


class DataConfig:
    """Data-specific configuration."""
    
    # Expected columns in raw data
    EXPECTED_COLUMNS = {
        'member_id': 'str',
        'age': 'int',
        'gender': 'str',
        'location': 'str',
        'cost': 'float',
        'visits': 'int',
        'er_visits': 'int',
        'hospitalizations': 'int',
        'diagnoses': 'str'
    }
    
    # Data quality thresholds
    MIN_RECORDS = 100
    MAX_MISSING_PCT = 0.5  # 50% max missing per column
    MIN_UNIQUE_VALUES = 2  # For categorical features
    
    # Outlier detection
    OUTLIER_METHOD = 'iqr'  # 'iqr' or 'zscore'
    OUTLIER_THRESHOLD = 3   # For zscore method


class ModelConfig:
    """Model-specific configuration."""
    
    # Cross-validation
    CV_FOLDS = 5
    CV_RANDOM_STATE = 42
    
    # Hyperparameter tuning
    GRID_SEARCH_CV = 5
    RANDOM_SEARCH_ITERATIONS = 20
    
    # Feature scaling
    SCALER_TYPE = 'standard'  # 'standard' or 'minmax'
    
    # Class imbalance handling
    HANDLE_IMBALANCE = False
    IMBALANCE_STRATEGY = 'smote'  # 'smote', 'undersampling', 'oversampling'


if __name__ == "__main__":
    print("Configuration loaded successfully")
    print(f"Project: {ProjectConfig.PROJECT_NAME}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Models directory: {MODELS_DIR}")
    print(f"Reports directory: {REPORTS_DIR}")
