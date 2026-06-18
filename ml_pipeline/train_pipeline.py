"""
Complete ML Pipeline: Training Script
Downloads dataset, preprocesses data, trains models, and saves the best model
"""
import os
import sys
import pandas as pd
import joblib
import logging
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor
from model_trainer import ModelTrainer
from eda import ExploratoryDataAnalysis

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLPipeline:
    """
    Complete ML pipeline from data loading to model deployment
    """
    
    def __init__(self, data_path=None, models_dir='../models', eda_dir='../eda_report'):
        """
        Initialize the ML Pipeline
        
        Args:
            data_path: Path to the dataset CSV file
            models_dir: Directory to save trained models
            eda_dir: Directory to save EDA reports
        """
        self.data_path = data_path
        self.models_dir = models_dir
        self.eda_dir = eda_dir
        self.data_processor = DataProcessor()
        self.model_trainer = None
        self.eda = ExploratoryDataAnalysis()
        
        # Create directories
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(eda_dir, exist_ok=True)
        
    def download_dataset(self):
        """
        Download the Telco Customer Churn dataset from Kaggle
        Note: Requires kaggle API configuration
        """
        logger.info("Downloading dataset from Kaggle...")
        try:
            import subprocess
            os.makedirs('data', exist_ok=True)
            
            # This requires kaggle API setup. For manual download:
            logger.info("""
            To download the Telco Customer Churn dataset:
            1. Go to https://www.kaggle.com/datasets/blastchar/telco-customer-churn
            2. Download the CSV file
            3. Place it in the 'data' folder as 'WA_Fn-UseC_-Telco-Customer-Churn.csv'
            
            Or use Kaggle API:
            - Setup: kaggle config set -n api_key
            - Download: kaggle datasets download -d blastchar/telco-customer-churn
            """)
            
            # Automated download using kaggle API (if available)
            subprocess.run(['kaggle', 'datasets', 'download', 
                          '-d', 'blastchar/telco-customer-churn', 
                          '-p', 'data'], check=False)
            
            # Unzip if needed
            import zipfile
            zip_files = [f for f in os.listdir('data') if f.endswith('.zip')]
            for zip_file in zip_files:
                with zipfile.ZipFile(os.path.join('data', zip_file), 'r') as zip_ref:
                    zip_ref.extractall('data')
                os.remove(os.path.join('data', zip_file))
            
            logger.info("Dataset downloaded successfully")
            
        except Exception as e:
            logger.warning(f"Automatic download failed: {e}. Please download manually.")
    
    def load_and_prepare_data(self):
        """
        Load and prepare the dataset
        
        Returns:
            Tuple of (X, y) - features and target
        """
        logger.info("Loading and preparing data...")
        
        # Load data
        if not self.data_path:
            # Try to find the dataset
            possible_paths = [
                'data/WA_Fn-UseC_-Telco-Customer-Churn.csv',
                '../data/WA_Fn-UseC_-Telco-Customer-Churn.csv',
                '../../data/WA_Fn-UseC_-Telco-Customer-Churn.csv'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.data_path = path
                    break
            
            if not self.data_path:
                raise FileNotFoundError("Dataset not found. Please download it first.")
        
        df = self.data_processor.load_data(self.data_path)
        
        # Rename columns to match database schema
        df = df.rename(columns={
            'gender': 'gender',
            'SeniorCitizen': 'age',  # Approximation
            'tenure': 'tenure_months',
            'PhoneService': 'phone_service',
            'InternetService': 'internet_service',
            'OnlineSecurity': 'online_security',
            'OnlineBackup': 'online_backup',
            'DeviceProtection': 'device_protection',
            'TechSupport': 'tech_support',
            'StreamingTV': 'streaming_tv',
            'StreamingMovies': 'streaming_movies',
            'Contract': 'contract',
            'PaperlessBilling': 'paperless_billing',
            'PaymentMethod': 'payment_method',
            'MonthlyCharges': 'monthly_charges',
            'TotalCharges': 'total_charges'
        }, errors='ignore')
        
        # Generate EDA report
        self.eda.generate_eda_report(df, target_column='Churn', output_dir=self.eda_dir)
        
        # Separate features and target
        target_column = 'Churn'
        y = df[target_column].map({'Yes': 1, 'No': 0}) if target_column in df.columns else None
        
        if y is None:
            raise ValueError(f"Target column '{target_column}' not found in dataset")
        
        # Preprocess features
        X = self.data_processor.preprocess(df.drop(columns=[target_column], errors='ignore'), 
                                          target_column=target_column, fit=True)
        
        logger.info(f"Data preparation completed. X shape: {X.shape}, y shape: {y.shape}")
        return X, y
    
    def train_models(self, X, y):
        """
        Train all models
        
        Args:
            X: Feature matrix
            y: Target vector
        """
        logger.info("Training models...")
        
        # Initialize trainer
        self.model_trainer = ModelTrainer(test_size=0.2, random_state=42)
        
        # Split data
        self.model_trainer.split_data(X, y)
        
        # Train all models
        self.model_trainer.train_all_models()
        
        # Evaluate all models
        self.model_trainer.evaluate_all_models()
        
        # Select best model
        best_model_name = self.model_trainer.select_best_model()
        
        logger.info(f"Best model: {best_model_name}")
        return best_model_name
    
    def save_models(self):
        """Save trained models and transformers"""
        logger.info("Saving models and transformers...")
        
        # Save best model
        self.model_trainer.save_model(os.path.join(self.models_dir, 'best_model.pkl'))
        
        # Save scaler
        joblib.dump(self.data_processor.scaler, 
                   os.path.join(self.models_dir, 'scaler.pkl'))
        
        # Save label encoders
        joblib.dump(self.data_processor.label_encoders, 
                   os.path.join(self.models_dir, 'encoder.pkl'))
        
        # Save feature columns
        joblib.dump(self.data_processor.feature_columns, 
                   os.path.join(self.models_dir, 'feature_columns.pkl'))
        
        logger.info(f"Models saved to {self.models_dir}")
    
    def generate_report(self):
        """Generate training report"""
        logger.info("Generating training report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'best_model': self.model_trainer.best_model_name,
            'performance_metrics': self.model_trainer.get_metrics_summary(),
            'comparison': self.model_trainer.get_performance_comparison().to_dict()
        }
        
        # Save report
        report_path = os.path.join(self.models_dir, 'training_report.txt')
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CUSTOMER CHURN PREDICTION - MODEL TRAINING REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Training Date: {report['timestamp']}\n")
            f.write(f"Best Model: {report['best_model']}\n\n")
            f.write("Performance Metrics:\n")
            f.write("-" * 80 + "\n")
            
            for model_name, metrics in report['performance_metrics'].items():
                f.write(f"\n{model_name}:\n")
                f.write(f"  Accuracy:  {metrics['accuracy']}\n")
                f.write(f"  Precision: {metrics['precision']}\n")
                f.write(f"  Recall:    {metrics['recall']}\n")
                f.write(f"  F1 Score:  {metrics['f1_score']}\n")
                f.write(f"  ROC-AUC:   {metrics['roc_auc']}\n")
        
        logger.info(f"Report saved to {report_path}")
        return report
    
    def run(self):
        """Execute the complete ML pipeline"""
        logger.info("Starting ML Pipeline...")
        
        try:
            # Step 1: Download dataset (if needed)
            if not os.path.exists(self.data_path or 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
                self.download_dataset()
            
            # Step 2: Load and prepare data
            X, y = self.load_and_prepare_data()
            
            # Step 3: Train models
            best_model = self.train_models(X, y)
            
            # Step 4: Save models
            self.save_models()
            
            # Step 5: Generate report
            report = self.generate_report()
            
            logger.info("ML Pipeline completed successfully!")
            return report
            
        except Exception as e:
            logger.error(f"Error in ML Pipeline: {str(e)}")
            raise


def main():
    """Main execution function"""
    # Check if data file exists
    data_file = 'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    
    if not os.path.exists(data_file):
        logger.info(f"\nDataset not found at {data_file}")
        logger.info("Please download the Telco Customer Churn dataset from:")
        logger.info("https://www.kaggle.com/datasets/blastchar/telco-customer-churn")
        logger.info(f"\nPlace the CSV file in the 'data' directory as 'WA_Fn-UseC_-Telco-Customer-Churn.csv'")
        sys.exit(1)
    
    # Initialize and run pipeline
    pipeline = MLPipeline(data_path=data_file)
    report = pipeline.run()
    
    print("\n" + "="*80)
    print("TRAINING REPORT")
    print("="*80)
    print(f"Best Model: {report['best_model']}")
    print("\nPerformance Comparison:")
    print(pipeline.model_trainer.get_performance_comparison().to_string())


if __name__ == '__main__':
    main()
