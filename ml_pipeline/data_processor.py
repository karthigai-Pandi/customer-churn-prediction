"""
ML Pipeline: Data Preprocessing and Preparation
Handles data loading, cleaning, and feature engineering
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Handles all data preprocessing tasks including:
    - Loading data
    - Handling missing values
    - Removing duplicates
    - Encoding categorical variables
    - Scaling numerical features
    """
    
    def __init__(self):
        """Initialize the DataProcessor"""
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.categorical_columns = []
        self.numerical_columns = []
        self.feature_columns = []
        
    def load_data(self, filepath):
        """
        Load CSV data from filepath
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame containing loaded data
        """
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def handle_missing_values(self, df):
        """
        Handle missing values in the dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info(f"Initial missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
        
        # For TotalCharges, convert to numeric and fill NaN with 0
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df['TotalCharges'].fillna(df['MonthlyCharges'], inplace=True)
        
        # Fill other missing values with mode for categorical, median for numerical
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype == 'object':
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    df[col].fillna(df[col].median(), inplace=True)
        
        logger.info("Missing values handled successfully")
        return df
    
    def remove_duplicates(self, df):
        """
        Remove duplicate records from the dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_shape = df.shape[0]
        df = df.drop_duplicates()
        removed = initial_shape - df.shape[0]
        logger.info(f"Removed {removed} duplicate records")
        return df
    
    def identify_column_types(self, df, target_column='Churn'):
        """
        Identify categorical and numerical columns
        
        Args:
            df: Input DataFrame
            target_column: Name of target column
            
        Returns:
            None (updates instance variables)
        """
        self.categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        self.numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target column from feature lists
        if target_column in self.categorical_columns:
            self.categorical_columns.remove(target_column)
        if target_column in self.numerical_columns:
            self.numerical_columns.remove(target_column)
        
        logger.info(f"Categorical columns: {self.categorical_columns}")
        logger.info(f"Numerical columns: {self.numerical_columns}")
    
    def encode_categorical_features(self, df, fit=True):
        """
        Encode categorical features using LabelEncoder
        
        Args:
            df: Input DataFrame
            fit: If True, fit the encoders; if False, use fitted encoders
            
        Returns:
            DataFrame with encoded categorical features
        """
        df = df.copy()
        
        for col in self.categorical_columns:
            if col not in df.columns:
                continue
                
            if fit:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
            else:
                df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        logger.info("Categorical features encoded successfully")
        return df
    
    def scale_numerical_features(self, df, fit=True):
        """
        Scale numerical features using StandardScaler
        
        Args:
            df: Input DataFrame
            fit: If True, fit the scaler; if False, use fitted scaler
            
        Returns:
            DataFrame with scaled numerical features
        """
        df = df.copy()
        
        if self.numerical_columns:
            if fit:
                df[self.numerical_columns] = self.scaler.fit_transform(df[self.numerical_columns])
            else:
                df[self.numerical_columns] = self.scaler.transform(df[self.numerical_columns])
        
        logger.info("Numerical features scaled successfully")
        return df
    
    def preprocess(self, df, target_column='Churn', fit=True):
        """
        Complete preprocessing pipeline
        
        Args:
            df: Input DataFrame
            target_column: Name of target column
            fit: If True, fit all transformers; if False, use fitted transformers
            
        Returns:
            Processed DataFrame
        """
        # Step 1: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 2: Remove duplicates
        df = self.remove_duplicates(df)
        
        # Step 3: Identify column types
        if fit:
            self.identify_column_types(df, target_column)
            self.feature_columns = self.categorical_columns + self.numerical_columns
        
        # Step 4: Encode categorical features
        df = self.encode_categorical_features(df, fit=fit)
        
        # Step 5: Scale numerical features
        df = self.scale_numerical_features(df, fit=fit)
        
        logger.info("Preprocessing completed successfully")
        return df
    
    def get_features(self, df):
        """
        Get feature matrix (remove target column)
        
        Args:
            df: Input DataFrame
            
        Returns:
            Feature matrix
        """
        return df[self.feature_columns] if self.feature_columns else df
    
    def get_statistics(self, df):
        """
        Get descriptive statistics of the dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with statistics
        """
        return {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'describe': df.describe().to_dict()
        }
