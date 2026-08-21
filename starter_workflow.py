"""
DSC680-T301 Applied Data Science
Starter Notebook: Complete Project Workflow

This script demonstrates the complete workflow from data loading to model predictions.
Run this to see all capabilities in action.
"""

import sys
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import ProjectConfig, DATA_DIR, OUTPUT_DIR, MODELS_DIR, REPORTS_DIR
from data_collection import HealthcareDataLoader, HealthcareCostAnalyzer
from analysis_and_visualization import DataExplorer, HealthcareVisualizer, StatisticalAnalyzer, ReportGenerator
from model_development import FeatureEngineering, PredictiveModel
import logging
import pandas as pd
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ProjectConfig.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def main():
    """Execute complete project workflow."""
    
    print_header("DSC680-T301 HEALTHCARE COST PREDICTION PROJECT")
    print(f"Course: {ProjectConfig.PROJECT_NAME}")
    print(f"Author: {ProjectConfig.AUTHOR}")
    print(f"Instructor: {ProjectConfig.INSTRUCTOR}")
    
    # =========================================================================
    # SECTION 1: DATA COLLECTION
    # =========================================================================
    print_header("SECTION 1: DATA COLLECTION & VALIDATION")
    
    logger.info("Initializing data loader...")
    loader = HealthcareDataLoader(data_dir=str(DATA_DIR))
    
    # TODO: Load your healthcare datasets
    logger.info("""
    Ready to load healthcare datasets!
    
    Place your datasets in: {}/
    Then uncomment the load_dataset calls below:
    
    df_members = loader.load_dataset(str(DATA_DIR / "members.csv"), "members")
    df_claims = loader.load_dataset(str(DATA_DIR / "claims.csv"), "claims")
    df_diagnoses = loader.load_dataset(str(DATA_DIR / "diagnoses.csv"), "diagnoses")
    
    For demonstration, we'll create sample data...
    """.format(DATA_DIR))
    
    # Create sample healthcare data with a stronger, learnable cost relationship
    np.random.seed(42)
    n_members = 1000
    
    sample_data = pd.DataFrame({
        'member_id': range(1, n_members + 1),
        'age': np.random.randint(18, 85, n_members),
        'gender': np.random.choice(['M', 'F'], n_members),
        'visits': np.random.poisson(5, n_members),
        'er_visits': np.random.poisson(1, n_members),
        'hospitalizations': np.random.poisson(0.5, n_members),
    })
    
    gender_multiplier = np.where(sample_data['gender'] == 'F', 1.15, 1.0)
    sample_data['cost'] = (
        2500
        + 120 * sample_data['age']
        + 900 * sample_data['visits']
        + 3200 * sample_data['er_visits']
        + 7000 * sample_data['hospitalizations']
    ) * gender_multiplier + np.random.normal(0, 1200, n_members)
    
    sample_data['cost'] = sample_data['cost'].clip(lower=0)
    
    loader.datasets['sample'] = sample_data
    logger.info(f"✓ Loaded sample dataset: {sample_data.shape}")
    
    # Validate data
    logger.info("Validating data quality...")
    validation = loader.validate_dataset('sample')
    logger.info(f"✓ Validation complete")
    logger.info(f"  - Rows: {validation['shape'][0]}")
    logger.info(f"  - Columns: {validation['shape'][1]}")
    logger.info(f"  - Memory: {validation['memory_usage']:.2f} MB")
    logger.info(f"  - Duplicates: {validation['duplicates']}")
    
    # =========================================================================
    # SECTION 2: COST ANALYSIS
    # =========================================================================
    print_header("SECTION 2: HEALTHCARE COST ANALYSIS")
    
    df = sample_data
    analyzer = HealthcareCostAnalyzer(df, cost_column='cost')
    
    # Cost distribution
    logger.info("Analyzing cost distribution...")
    cost_dist = analyzer.analyze_cost_distribution()
    
    print(f"\nCost Statistics:")
    print(f"  Mean Cost: ${cost_dist['mean']:,.2f}")
    print(f"  Median Cost: ${cost_dist['median']:,.2f}")
    print(f"  Std Dev: ${cost_dist['std']:,.2f}")
    print(f"  Min: ${cost_dist['min']:,.2f}")
    print(f"  Max: ${cost_dist['max']:,.2f}")
    print(f"  95th Percentile: ${cost_dist['q95']:,.2f}")
    print(f"  Skewness: {cost_dist['skewness']:.2f}")
    
    # High-cost members
    high_cost = analyzer.identify_high_cost_members(percentile=90)
    logger.info(f"✓ Identified {len(high_cost)} high-cost members (90th percentile)")
    
    # Cost concentration
    concentration = analyzer.calculate_cost_concentration()
    print(f"\nCost Concentration (Pareto Analysis):")
    print(f"  Total Cost: ${concentration['total_cost']:,.0f}")
    print(f"  {concentration['pct_members_for_80_pct_cost']:.1f}% of members account for 80% of costs")
    print(f"  Top 10% of members account for: {concentration['top_10_pct_contribution']:.1f}% of costs")
    print(f"  Top 20% of members account for: {concentration['top_20_pct_contribution']:.1f}% of costs")
    
    # =========================================================================
    # SECTION 3: EXPLORATORY DATA ANALYSIS
    # =========================================================================
    print_header("SECTION 3: EXPLORATORY DATA ANALYSIS")
    
    explorer = DataExplorer(df)
    
    # Generate overview
    print(explorer.generate_overview())
    
    # Numeric analysis
    logger.info("Analyzing numeric columns...")
    numeric_analysis = explorer.analyze_numeric_columns()
    print("\nNumeric Columns Summary:")
    print(numeric_analysis)
    
    # Categorical analysis
    logger.info("Analyzing categorical columns...")
    categorical_analysis = explorer.analyze_categorical_columns()
    print("\nCategorical Columns Summary:")
    for col, analysis in categorical_analysis.items():
        print(f"\n{col}:")
        print(f"  Unique values: {analysis['unique_values']}")
        print(f"  Top values: {analysis['top_values']}")
    
    # Correlation analysis
    logger.info("Calculating correlations...")
    correlation = explorer.correlation_analysis()
    print("\nCorrelation with Cost:")
    print(correlation['cost'].sort_values(ascending=False))
    
    # =========================================================================
    # SECTION 4: DATA VISUALIZATION
    # =========================================================================
    print_header("SECTION 4: DATA VISUALIZATION")
    
    visualizer = HealthcareVisualizer()
    
    logger.info("Creating visualizations...")
    
    # Cost distribution
    fig1 = visualizer.plot_cost_distribution(df['cost'])
    output_file = str(OUTPUT_DIR / "cost_distribution.png")
    fig1.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"✓ Saved: {output_file}")
    
    # Pareto analysis
    fig2 = visualizer.plot_pareto_analysis(df['cost'])
    output_file = str(OUTPUT_DIR / "pareto_analysis.png")
    fig2.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"✓ Saved: {output_file}")
    
    # Correlation heatmap
    fig3 = visualizer.plot_correlation_heatmap(correlation)
    output_file = str(OUTPUT_DIR / "correlation_heatmap.png")
    fig3.savefig(output_file, dpi=300, bbox_inches='tight')
    logger.info(f"✓ Saved: {output_file}")
    
    print("\n✓ Visualizations saved to output/ directory")
    
    # =========================================================================
    # SECTION 5: FEATURE ENGINEERING
    # =========================================================================
    print_header("SECTION 5: FEATURE ENGINEERING")
    
    fe = FeatureEngineering(df)
    
    logger.info("Creating demographic features...")
    fe.create_demographic_features()
    logger.info("✓ Added demographic features")
    
    logger.info("Creating utilization features...")
    fe.create_utilization_features()
    logger.info("✓ Added utilization features")
    
    logger.info("Creating interaction features...")
    fe.create_interaction_features()
    logger.info("✓ Added interaction features")
    
    logger.info("Encoding categorical features...")
    fe.encode_categorical_features(['gender'])
    logger.info("✓ Encoded categorical features")
    
    logger.info("Handling missing values...")
    df_clean = fe.handle_missing_values(strategy='median')
    logger.info("✓ Missing values handled")
    
    df_engineered = df_clean.copy()
    logger.info(f"✓ Feature engineering complete")
    print(f"\nEngineered dataset shape: {df_engineered.shape}")
    print(f"Sample of engineered features:\n{df_engineered.head()}")
    
    # =========================================================================
    # SECTION 6: MODEL DEVELOPMENT
    # =========================================================================
    print_header("SECTION 6: MODEL DEVELOPMENT & TRAINING")
    
    # Prepare features and target
    X = df_engineered.drop('cost', axis=1).select_dtypes(include=[np.number]).copy()
    y = df_engineered['cost']
    
    logger.info(f"Feature matrix shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")
    
    # Initialize model framework
    model = PredictiveModel(X, y, test_size=0.2)
    
    # Train models
    print("\nTraining models...")
    print("-" * 70)
    
    logger.info("Training Linear Regression...")
    lr_results = model.train_linear_regression()
    print(f"✓ Linear Regression    R²={lr_results['r2_score']:.4f}  RMSE=${lr_results['rmse']:,.0f}")
    
    logger.info("Training Ridge Regression...")
    ridge_results = model.train_ridge_regression(alpha=1.0)
    print(f"✓ Ridge Regression     R²={ridge_results['r2_score']:.4f}  RMSE=${ridge_results['rmse']:,.0f}")
    
    logger.info("Training Random Forest...")
    rf_results = model.train_random_forest(n_estimators=100, max_depth=10)
    print(f"✓ Random Forest        R²={rf_results['r2_score']:.4f}  RMSE=${rf_results['rmse']:,.0f}")
    
    logger.info("Training Gradient Boosting...")
    gb_results = model.train_gradient_boosting(n_estimators=100, learning_rate=0.1)
    print(f"✓ Gradient Boosting    R²={gb_results['r2_score']:.4f}  RMSE=${gb_results['rmse']:,.0f}")
    
    print("-" * 70)
    
    # =========================================================================
    # SECTION 7: MODEL EVALUATION
    # =========================================================================
    print_header("SECTION 7: MODEL EVALUATION & SELECTION")
    
    best_model_name, best_results = model.get_best_model()
    
    print(f"\n🏆 Best Model: {best_model_name.upper()}")
    print(f"\nPerformance Metrics:")
    print(f"  R² Score: {best_results['r2_score']:.4f} (explains {best_results['r2_score']*100:.1f}% of variance)")
    print(f"  RMSE: ${best_results['rmse']:,.2f}")
    print(f"  MAE: ${best_results['mae']:,.2f}")
    print(f"  MSE: ${best_results['mse']:,.2f}")
    
    # Feature importance (if available)
    if 'feature_importance' in best_results:
        print(f"\nTop 10 Most Important Features:")
        feature_imp = best_results['feature_importance']
        for idx, row in feature_imp.head(10).iterrows():
            print(f"  {row['feature']:20s} {row['importance']:.4f}")
    
    # =========================================================================
    # SECTION 8: PREDICTIONS & INSIGHTS
    # =========================================================================
    print_header("SECTION 8: PREDICTIONS & MEMBER INSIGHTS")
    
    predictions = best_results['predictions']
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'actual_cost': y.iloc[model.X_test.index].values,
        'predicted_cost': predictions,
        'prediction_error': y.iloc[model.X_test.index].values - predictions
    })
    
    print(f"\nPrediction Statistics (Test Set):")
    print(f"  Mean Actual Cost: ${results_df['actual_cost'].mean():,.2f}")
    print(f"  Mean Predicted Cost: ${results_df['predicted_cost'].mean():,.2f}")
    print(f"  Mean Error: ${results_df['prediction_error'].mean():,.2f}")
    print(f"  Median Error: ${results_df['prediction_error'].median():,.2f}")
    
    # Save results
    results_df.to_csv(str(OUTPUT_DIR / "predictions.csv"), index=False)
    logger.info(f"✓ Predictions saved to: {OUTPUT_DIR / 'predictions.csv'}")
    
    # =========================================================================
    # SECTION 9: SAVE ARTIFACTS
    # =========================================================================
    print_header("SECTION 9: SAVING ARTIFACTS")
    
    # Save best model
    model_path = ProjectConfig.get_model_path(best_model_name)
    model.save_model(best_model_name, str(model_path))
    logger.info(f"✓ Model saved to: {model_path}")
    
    # Save validation report
    report_path = str(OUTPUT_DIR / "data_validation_report.json")
    loader.export_validation_report(report_path)
    logger.info(f"✓ Validation report saved to: {report_path}")
    
    # =========================================================================
    # COMPLETION
    # =========================================================================
    print_header("PROJECT WORKFLOW COMPLETE ✅")
    
    print(f"""
    Summary:
    --------
    ✓ Data loaded and validated
    ✓ Cost analysis completed
    ✓ Exploratory analysis done
    ✓ 4 models trained and compared
    ✓ Best model: {best_model_name} (R²={best_results['r2_score']:.4f})
    ✓ Predictions generated for {len(predictions)} test members
    ✓ All artifacts saved to project directories
    
    Output Files:
    - output/cost_distribution.png
    - output/pareto_analysis.png
    - output/correlation_heatmap.png
    - output/predictions.csv
    - output/data_validation_report.json
    - models/{best_model_name}.pkl
    - project.log
    
    Next Steps:
    1. Review the generated visualizations
    2. Examine predictions vs actual costs
    3. Analyze feature importance
    4. Experiment with hyperparameter tuning
    5. Deploy model for production use
    
    For more details, see:
    - README.md - Project overview
    - IMPLEMENTATION_GUIDE.md - Detailed usage guide
    - config.py - Configuration settings
    """)
    
    logger.info("✅ Project workflow complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error in workflow: {str(e)}", exc_info=True)
        raise
