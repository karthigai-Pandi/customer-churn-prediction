"""
ML Pipeline: Model Training and Comparison
Trains multiple models and evaluates their performance
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, confusion_matrix, roc_curve)
import xgboost as xgb
import joblib
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Handles model training, evaluation, and comparison
    Trains multiple algorithms and selects the best performer
    """
    
    def __init__(self, test_size=0.2, random_state=42):
        """
        Initialize the ModelTrainer
        
        Args:
            test_size: Proportion of data for testing
            random_state: Random state for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.performance_metrics = {}
        self.best_model = None
        self.best_model_name = None
        
    def split_data(self, X, y):
        """
        Split data into training and testing sets
        
        Args:
            X: Feature matrix
            y: Target vector
            
        Returns:
            None (updates instance variables)
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        logger.info(f"Data split: Train size = {self.X_train.shape[0]}, Test size = {self.X_test.shape[0]}")
    
    def train_logistic_regression(self):
        """Train Logistic Regression model"""
        logger.info("Training Logistic Regression...")
        model = LogisticRegression(max_iter=1000, random_state=self.random_state)
        model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = model
        logger.info("Logistic Regression trained successfully")
    
    def train_decision_tree(self):
        """Train Decision Tree model"""
        logger.info("Training Decision Tree...")
        model = DecisionTreeClassifier(max_depth=10, min_samples_split=10, 
                                      min_samples_leaf=5, random_state=self.random_state)
        model.fit(self.X_train, self.y_train)
        self.models['Decision Tree'] = model
        logger.info("Decision Tree trained successfully")
    
    def train_random_forest(self):
        """Train Random Forest model"""
        logger.info("Training Random Forest...")
        model = RandomForestClassifier(n_estimators=100, max_depth=15, 
                                      min_samples_split=10, min_samples_leaf=5,
                                      random_state=self.random_state, n_jobs=-1)
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        logger.info("Random Forest trained successfully")
    
    def train_xgboost(self):
        """Train XGBoost model"""
        logger.info("Training XGBoost...")
        model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1,
                                 random_state=self.random_state, use_label_encoder=False,
                                 eval_metric='logloss', verbosity=0)
        model.fit(self.X_train, self.y_train)
        self.models['XGBoost'] = model
        logger.info("XGBoost trained successfully")
    
    def evaluate_model(self, model_name):
        """
        Evaluate a trained model
        
        Args:
            model_name: Name of the model to evaluate
            
        Returns:
            Dictionary containing performance metrics
        """
        model = self.models[model_name]
        y_pred = model.predict(self.X_test)
        y_pred_proba = model.predict_proba(self.X_test)[:, 1]
        
        metrics = {
            'model_name': model_name,
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, zero_division=0),
            'recall': recall_score(self.y_test, y_pred, zero_division=0),
            'f1_score': f1_score(self.y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(self.y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(self.y_test, y_pred).tolist(),
            'y_pred': y_pred.tolist(),
            'y_pred_proba': y_pred_proba.tolist(),
            'training_date': datetime.now().isoformat(),
            'data_size': len(self.y_test)
        }
        
        self.performance_metrics[model_name] = metrics
        logger.info(f"{model_name} - Accuracy: {metrics['accuracy']:.4f}, ROC-AUC: {metrics['roc_auc']:.4f}")
        return metrics
    
    def train_all_models(self):
        """Train all models"""
        logger.info("Training all models...")
        self.train_logistic_regression()
        self.train_decision_tree()
        self.train_random_forest()
        self.train_xgboost()
        logger.info("All models trained successfully")
    
    def evaluate_all_models(self):
        """Evaluate all trained models"""
        logger.info("Evaluating all models...")
        for model_name in self.models.keys():
            self.evaluate_model(model_name)
        logger.info("All models evaluated successfully")
    
    def select_best_model(self):
        """
        Select the best performing model based on ROC-AUC score
        
        Returns:
            Best model name
        """
        best_score = -1
        best_name = None
        
        for model_name, metrics in self.performance_metrics.items():
            if metrics['roc_auc'] > best_score:
                best_score = metrics['roc_auc']
                best_name = model_name
        
        self.best_model = self.models[best_name]
        self.best_model_name = best_name
        logger.info(f"Best model selected: {best_name} (ROC-AUC: {best_score:.4f})")
        return best_name
    
    def get_performance_comparison(self):
        """
        Get comparison of all models
        
        Returns:
            DataFrame with performance metrics
        """
        comparison_data = []
        for model_name, metrics in self.performance_metrics.items():
            comparison_data.append({
                'Model': model_name,
                'Accuracy': f"{metrics['accuracy']:.4f}",
                'Precision': f"{metrics['precision']:.4f}",
                'Recall': f"{metrics['recall']:.4f}",
                'F1 Score': f"{metrics['f1_score']:.4f}",
                'ROC-AUC': f"{metrics['roc_auc']:.4f}"
            })
        return pd.DataFrame(comparison_data)
    
    def save_model(self, filepath):
        """
        Save the best model using joblib
        
        Args:
            filepath: Path to save the model
        """
        joblib.dump(self.best_model, filepath)
        logger.info(f"Best model saved to {filepath}")
    
    def get_metrics_summary(self):
        """
        Get summary of all metrics
        
        Returns:
            Dictionary with metrics summary
        """
        summary = {}
        for model_name, metrics in self.performance_metrics.items():
            summary[model_name] = {
                'accuracy': round(metrics['accuracy'], 4),
                'precision': round(metrics['precision'], 4),
                'recall': round(metrics['recall'], 4),
                'f1_score': round(metrics['f1_score'], 4),
                'roc_auc': round(metrics['roc_auc'], 4),
                'confusion_matrix': metrics['confusion_matrix']
            }
        return summary
