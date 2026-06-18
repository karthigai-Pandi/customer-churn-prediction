"""
Synthetic Customer Churn Dataset Generator
Creates a realistic telecom customer churn dataset for model training
"""

import pandas as pd
import numpy as np
import os

def generate_churn_dataset(n_samples=5000, output_path='data/churn_data.csv'):
    """
    Generate synthetic customer churn dataset
    
    Args:
        n_samples: Number of customer records to generate
        output_path: Path to save the CSV file
    """
    np.random.seed(42)
    
    # Generate customer data
    data = {
        'customer_id': [f'CUST{i:05d}' for i in range(n_samples)],
        'age': np.random.randint(18, 80, n_samples),
        'tenure_months': np.random.randint(1, 72, n_samples),
        'monthly_charges': np.random.uniform(20, 150, n_samples),
        'total_charges': np.random.uniform(20, 8000, n_samples),
        'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'online_security': np.random.choice(['Yes', 'No'], n_samples),
        'online_backup': np.random.choice(['Yes', 'No'], n_samples),
        'device_protection': np.random.choice(['Yes', 'No'], n_samples),
        'tech_support': np.random.choice(['Yes', 'No'], n_samples),
        'streaming_tv': np.random.choice(['Yes', 'No'], n_samples),
        'streaming_movies': np.random.choice(['Yes', 'No'], n_samples),
        'contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'paperless_billing': np.random.choice(['Yes', 'No'], n_samples),
        'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'gender': np.random.choice(['Male', 'Female'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create churn target (higher charges and shorter tenure = more likely to churn)
    churn_probability = (
        (1 - df['tenure_months'] / 72) * 0.5 +  # Tenure factor
        (df['monthly_charges'] / 150) * 0.3 +     # Charges factor
        (df['internet_service'] == 'Fiber optic').astype(int) * 0.15 +  # Service factor
        np.random.normal(0, 0.1, n_samples)  # Random noise
    )
    
    # Ensure probabilities are between 0 and 1
    churn_probability = np.clip(churn_probability, 0, 1)
    
    # Generate churn labels
    df['churn'] = (churn_probability > 0.5).astype(int)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"✓ Generated {n_samples} customer records")
    print(f"✓ Saved to {output_path}")
    print(f"✓ Churn rate: {df['churn'].mean():.1%}")
    print(f"✓ Dataset shape: {df.shape}")
    
    return df

if __name__ == '__main__':
    generate_churn_dataset(n_samples=5000)
    print("\n✓ Data generation complete!")
