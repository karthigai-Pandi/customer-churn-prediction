"""
Machine Learning Model Training and Prediction Pipeline
Trains churn prediction models and provides prediction interface
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve, auc
)
import joblib
import os

class ChurnPredictor:
    """Churn prediction model with training and inference capabilities"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoders = {}
        self.feature_columns = None
        self.metrics = {}
        
    def load_data(self, filepath):
        """Load dataset from CSV"""
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {len(df)} records from {filepath}")
        return df
    
    def preprocess(self, df):
        """Preprocess data: encoding, scaling, feature selection"""
        df_processed = df.copy()
        
        # Identify categorical and numerical columns
        categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
        numerical_cols = df_processed.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        # Remove target variable and ID columns from processing
        for col in ['churn', 'customer_id']:
            if col in categorical_cols:
                categorical_cols.remove(col)
            if col in numerical_cols:
                numerical_cols.remove(col)
        
        # Encode categorical features
        for col in categorical_cols:
            encoder = LabelEncoder()
            df_processed[col] = encoder.fit_transform(df_processed[col])
            self.encoders[col] = encoder
        
        # Scale numerical features
        if not self.scaler:
            self.scaler = StandardScaler()
            df_processed[numerical_cols] = self.scaler.fit_transform(df_processed[numerical_cols])
        else:
            df_processed[numerical_cols] = self.scaler.transform(df_processed[numerical_cols])
        
        self.feature_columns = [col for col in df_processed.columns if col not in ['churn', 'customer_id']]
        
        print(f"✓ Preprocessed data: {len(self.feature_columns)} features")
        return df_processed
    
    def train(self, df):
        """Train churn prediction model"""
        X = df[self.feature_columns]
        y = df['churn'].astype(int)  # Ensure target is integer type
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"✓ Train set: {len(X_train)}, Test set: {len(X_test)}")
        
        # Train Random Forest (best performance/simplicity tradeoff)
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        print("✓ Model trained successfully")
        
        # Evaluate
        self._evaluate(X_test, y_test)
        
        # Compare with other models
        self._compare_models(X_train, X_test, y_train, y_test)
        
        return self.metrics
    
    def _evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        self.metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        }
        
        print(f"\n{'='*50}")
        print("MODEL PERFORMANCE METRICS")
        print(f"{'='*50}")
        print(f"Accuracy:  {self.metrics['accuracy']:.1%}")
        print(f"Precision: {self.metrics['precision']:.1%}")
        print(f"Recall:    {self.metrics['recall']:.1%}")
        print(f"F1 Score:  {self.metrics['f1']:.1%}")
        print(f"ROC-AUC:   {self.metrics['roc_auc']:.1%}")
        print(f"{'='*50}\n")
    
    def _compare_models(self, X_train, X_test, y_train, y_test):
        """Compare performance of multiple algorithms"""
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'XGBoost': XGBClassifier(n_estimators=100, random_state=42, verbosity=0)
        }
        
        print(f"\n{'='*60}")
        print("MODEL COMPARISON")
        print(f"{'='*60}")
        
        results = []
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            result = {
                'Model': name,
                'Accuracy': accuracy_score(y_test, y_pred),
                'ROC-AUC': roc_auc_score(y_test, y_pred_proba),
            }
            results.append(result)
        
        results_df = pd.DataFrame(results).sort_values('ROC-AUC', ascending=False)
        print(results_df.to_string(index=False))
        print(f"{'='*60}\n")
    
    def predict(self, input_data):
        """
        Make prediction for new customer
        
        Args:
            input_data: Dictionary with customer features
            
        Returns:
            Dictionary with prediction and probability
        """
        # Create DataFrame with single row
        df = pd.DataFrame([input_data])
        
        # Process using stored encoders and scaler
        for col, encoder in self.encoders.items():
            if col in df.columns:
                df[col] = encoder.transform(df[col])
        
        numerical_cols = [col for col in df.columns if col not in self.encoders.keys()]
        if numerical_cols:
            df[numerical_cols] = self.scaler.transform(df[numerical_cols])
        
        # Make prediction
        X = df[self.feature_columns]
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0][1]
        
        return {
            'prediction': int(prediction),
            'will_churn': bool(prediction),
            'churn_probability': float(probability),
            'risk_level': 'HIGH' if probability > 0.6 else 'LOW'
        }
    
    def save_model(self, model_dir='models'):
        """Save trained model and preprocessing objects"""
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(self.model, os.path.join(model_dir, 'churn_model.pkl'))
        joblib.dump(self.scaler, os.path.join(model_dir, 'scaler.pkl'))
        joblib.dump(self.encoders, os.path.join(model_dir, 'encoders.pkl'))
        joblib.dump(self.feature_columns, os.path.join(model_dir, 'features.pkl'))
        
        print(f"✓ Model saved to {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """Load pre-trained model and preprocessing objects"""
        self.model = joblib.load(os.path.join(model_dir, 'churn_model.pkl'))
        self.scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        self.encoders = joblib.load(os.path.join(model_dir, 'encoders.pkl'))
        self.feature_columns = joblib.load(os.path.join(model_dir, 'features.pkl'))
        
        print(f"✓ Model loaded from {model_dir}/")

def main():
    """Training pipeline"""
    predictor = ChurnPredictor()
    
    # Load data
    df = predictor.load_data('data/churn_data.csv')
    
    # Preprocess
    df_processed = predictor.preprocess(df)
    
    # Train
    metrics = predictor.train(df_processed)
    
    # Save
    predictor.save_model()
    
    # Example prediction
    print("\nExample Prediction:")
    sample_customer = {
        'age': 45,
        'tenure_months': 24,
        'monthly_charges': 75.5,
        'total_charges': 1800,
        'internet_service': 'Fiber optic',
        'online_security': 'Yes',
        'online_backup': 'No',
        'device_protection': 'No',
        'tech_support': 'Yes',
        'streaming_tv': 'Yes',
        'streaming_movies': 'No',
        'contract': 'Month-to-month',
        'paperless_billing': 'Yes',
        'payment_method': 'Electronic check',
        'gender': 'Male',
    }
    
    result = predictor.predict(sample_customer)
    print(f"Will Churn: {result['will_churn']}")
    print(f"Probability: {result['churn_probability']:.1%}")
    print(f"Risk Level: {result['risk_level']}")

if __name__ == '__main__':
    main()
