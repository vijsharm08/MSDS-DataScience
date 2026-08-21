"""
DSC680-T301 Applied Data Science
Model Development Module

This module provides the foundation for building predictive models
to identify high-cost healthcare members.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging
from typing import Tuple, Dict, List
import pickle

logger = logging.getLogger(__name__)


class FeatureEngineering:
    """
    Create and engineer features for the prediction model.
    """
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with DataFrame."""
        self.df = df.copy()
        self.engineered_features = {}
    
    def create_demographic_features(self) -> pd.DataFrame:
        """Create demographic-based features."""
        df = self.df
        
        if 'age' in df.columns:
            df['age_group'] = pd.cut(
                df['age'],
                bins=[0, 18, 35, 50, 65, 100],
                labels=['Child', 'Young Adult', 'Adult', 'Senior', 'Elderly'],
            )
        
        if 'conditions' in df.columns:
            df['num_conditions'] = df['conditions'].str.split(',').str.len()
        
        self.engineered_features['demographic'] = df
        return df
    
    def create_utilization_features(self) -> pd.DataFrame:
        """Create healthcare utilization features."""
        df = self.df
        
        if 'visits' in df.columns:
            df['visits_per_month'] = df['visits'] / 12
            df['is_frequent_visitor'] = (df['visits'] > df['visits'].quantile(0.75)).astype(int)
        
        if 'er_visits' in df.columns:
            df['has_er_visits'] = (df['er_visits'] > 0).astype(int)
        
        self.engineered_features['utilization'] = df
        return df
    
    def create_interaction_features(self) -> pd.DataFrame:
        """Create interaction features."""
        df = self.df
        
        if 'age' in df.columns and 'visits' in df.columns:
            df['age_visits_interaction'] = df['age'] * df['visits']
        
        self.engineered_features['interaction'] = df
        return df
    
    def handle_missing_values(self, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            strategy: 'mean', 'median', or 'drop'
        
        Returns:
            DataFrame with missing values handled
        """
        df = self.df
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if strategy == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'drop':
            df = df.dropna()
        
        logger.info(f"Missing values handled using '{strategy}' strategy")
        return df
    
    def encode_categorical_features(self, categorical_cols: List[str]) -> pd.DataFrame:
        """
        Encode categorical features.
        
        Args:
            categorical_cols: List of categorical column names
        
        Returns:
            DataFrame with encoded categorical features
        """
        df = self.df
        
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
        
        logger.info(f"Encoded {len(categorical_cols)} categorical features")
        return df


class PredictiveModel:
    """
    Build and train predictive models for cost prediction.
    """
    
    def __init__(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
        """
        Initialize model.
        
        Args:
            X: Features
            y: Target variable (cost)
            test_size: Proportion of data for testing
        """
        self.X = X
        self.y = y
        self.test_size = test_size
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        self.models = {}
        self.results = {}
        
        logger.info(f"Training set size: {len(self.X_train)}, Test set size: {len(self.X_test)}")
    
    def train_linear_regression(self) -> Dict:
        """Train linear regression model."""
        model = LinearRegression()
        model.fit(self.X_train_scaled, self.y_train)
        
        y_pred = model.predict(self.X_test_scaled)
        
        results = self._evaluate_model(y_pred, 'Linear Regression')
        
        self.models['linear_regression'] = model
        self.results['linear_regression'] = results
        
        return results
    
    def train_ridge_regression(self, alpha: float = 1.0) -> Dict:
        """Train ridge regression model."""
        model = Ridge(alpha=alpha)
        model.fit(self.X_train_scaled, self.y_train)
        
        y_pred = model.predict(self.X_test_scaled)
        
        results = self._evaluate_model(y_pred, f'Ridge Regression (alpha={alpha})')
        
        self.models['ridge_regression'] = model
        self.results['ridge_regression'] = results
        
        return results
    
    def train_lasso_regression(self, alpha: float = 0.1) -> Dict:
        """Train lasso regression model."""
        model = Lasso(alpha=alpha)
        model.fit(self.X_train_scaled, self.y_train)
        
        y_pred = model.predict(self.X_test_scaled)
        
        results = self._evaluate_model(y_pred, f'Lasso Regression (alpha={alpha})')
        
        self.models['lasso_regression'] = model
        self.results['lasso_regression'] = results
        
        return results
    
    def train_random_forest(self, n_estimators: int = 100, max_depth: int = 10) -> Dict:
        """Train random forest model."""
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, 
                                      random_state=42, n_jobs=-1)
        model.fit(self.X_train, self.y_train)
        
        y_pred = model.predict(self.X_test)
        
        results = self._evaluate_model(y_pred, 
                                      f'Random Forest (n_est={n_estimators}, depth={max_depth})')
        
        self.models['random_forest'] = model
        self.results['random_forest'] = results
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        results['feature_importance'] = feature_importance
        
        return results
    
    def train_gradient_boosting(self, n_estimators: int = 100, learning_rate: float = 0.1) -> Dict:
        """Train gradient boosting model."""
        model = GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate,
                                        random_state=42)
        model.fit(self.X_train, self.y_train)
        
        y_pred = model.predict(self.X_test)
        
        results = self._evaluate_model(y_pred, 
                                      f'Gradient Boosting (n_est={n_estimators}, lr={learning_rate})')
        
        self.models['gradient_boosting'] = model
        self.results['gradient_boosting'] = results
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        results['feature_importance'] = feature_importance
        
        return results
    
    def _evaluate_model(self, y_pred: np.ndarray, model_name: str) -> Dict:
        """Evaluate model performance."""
        mse = mean_squared_error(self.y_test, y_pred)
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        
        evaluation = {
            'model_name': model_name,
            'mse': mse,
            'mae': mae,
            'rmse': rmse,
            'r2_score': r2,
            'predictions': y_pred
        }
        
        logger.info(f"{model_name}: RMSE={rmse:.2f}, MAE={mae:.2f}, R²={r2:.4f}")
        
        return evaluation
    
    def get_best_model(self) -> Tuple[str, Dict]:
        """Get model with best R² score."""
        best_model_name = max(self.results.keys(), 
                             key=lambda x: self.results[x]['r2_score'])
        
        return best_model_name, self.results[best_model_name]
    
    def save_model(self, model_name: str, filepath: str):
        """Save model to file."""
        if model_name not in self.models:
            logger.error(f"Model '{model_name}' not found")
            return
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.models[model_name], f)
        
        logger.info(f"Model saved to: {filepath}")
    
    def load_model(self, model_name: str, filepath: str):
        """Load model from file."""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        self.models[model_name] = model
        logger.info(f"Model loaded from: {filepath}")
        
        return model
    
    def hyperparameter_tuning(self, model_type: str = 'random_forest') -> Dict:
        """
        Perform hyperparameter tuning.
        
        Args:
            model_type: Type of model to tune
        
        Returns:
            Dictionary with best parameters
        """
        if model_type == 'random_forest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10]
            }
            model = RandomForestRegressor(random_state=42)
        
        elif model_type == 'gradient_boosting':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.05, 0.1],
                'max_depth': [3, 5, 7]
            }
            model = GradientBoostingRegressor(random_state=42)
        
        else:
            logger.error(f"Model type '{model_type}' not supported")
            return {}
        
        grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, scoring='r2')
        grid_search.fit(self.X_train, self.y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'grid_search': grid_search
        }


if __name__ == "__main__":
    print("Healthcare Cost Prediction Model Development Module")
    print("Ready for use in model training and evaluation")
