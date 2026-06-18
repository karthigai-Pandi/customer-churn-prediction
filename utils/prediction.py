"""
Utility Functions: Prediction and Data Formatting
Handles model predictions and result formatting
"""
import joblib
import pandas as pd
import numpy as np
import logging
from config.config import get_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionEngine:
    """
    Handles loading models and making predictions
    """
    
    def __init__(self):
        """Initialize the prediction engine"""
        config = get_config()
        self.model = None
        self.scaler = None
        self.encoder = None
        self.feature_columns = None
        self.load_models()
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            config = get_config()
            
            self.model = joblib.load(config.MODEL_PATH)
            self.scaler = joblib.load(config.SCALER_PATH)
            self.encoder = joblib.load(config.ENCODER_PATH)
            self.feature_columns = joblib.load(config.FEATURE_COLUMNS_PATH)
            
            logger.info("Models loaded successfully")
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {str(e)}")
            logger.error("Please train the model first using ml_pipeline/train_pipeline.py")
            raise
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise
    
    def preprocess_input(self, input_data):
        """
        Preprocess input data for prediction
        
        Args:
            input_data: Dictionary with feature values
            
        Returns:
            Preprocessed feature matrix
        """
        try:
            # Create DataFrame from input
            df = pd.DataFrame([input_data])
            
            # Encode categorical features
            for col, encoder in self.encoder.items():
                if col in df.columns:
                    df[col] = encoder.transform(df[col].astype(str))
            
            # Select only required features
            df = df[self.feature_columns]
            
            # Scale numerical features
            df = pd.DataFrame(
                self.scaler.transform(df),
                columns=self.feature_columns
            )
            
            return df
        except Exception as e:
            logger.error(f"Error preprocessing input: {str(e)}")
            raise
    
    def predict(self, input_data):
        """
        Make prediction for input data
        
        Args:
            input_data: Dictionary with feature values
            
        Returns:
            Dictionary with prediction and probability
        """
        try:
            # Preprocess input
            processed_data = self.preprocess_input(input_data)
            
            # Make prediction
            prediction = self.model.predict(processed_data)[0]
            probability = self.model.predict_proba(processed_data)[0]
            
            # Calculate risk level
            churn_probability = probability[1]
            risk_level = 'High Risk' if churn_probability > 0.7 else 'Low Risk'
            
            result = {
                'churn_prediction': int(prediction),
                'churn_probability': round(churn_probability, 4),
                'risk_level': risk_level,
                'no_churn_probability': round(probability[0], 4),
                'confidence_score': round(max(probability), 4)
            }
            
            logger.info(f"Prediction made: {result}")
            return result
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def batch_predict(self, input_list):
        """
        Make predictions for multiple inputs
        
        Args:
            input_list: List of dictionaries with feature values
            
        Returns:
            List of predictions
        """
        results = []
        for input_data in input_list:
            result = self.predict(input_data)
            results.append(result)
        return results


def format_prediction_result(prediction_dict, customer_id=None, contract_id=None):
    """
    Format prediction result for API response
    
    Args:
        prediction_dict: Dictionary with prediction values
        customer_id: Customer ID
        contract_id: Contract ID
        
    Returns:
        Formatted dictionary
    """
    return {
        'customer_id': customer_id,
        'contract_id': contract_id,
        'churn_prediction': 'Yes' if prediction_dict['churn_prediction'] == 1 else 'No',
        'churn_probability': prediction_dict['churn_probability'],
        'risk_level': prediction_dict['risk_level'],
        'confidence_score': prediction_dict['confidence_score'],
        'message': f"Customer has {prediction_dict['risk_level']} for churn"
    }


def validate_input_data(input_data, required_fields):
    """
    Validate input data
    
    Args:
        input_data: Dictionary with input values
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    missing_fields = [field for field in required_fields if field not in input_data or not input_data[field]]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None
