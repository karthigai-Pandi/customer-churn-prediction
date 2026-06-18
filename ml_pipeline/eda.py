"""
ML Pipeline: Exploratory Data Analysis (EDA)
Generates visualizations and statistical analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExploratoryDataAnalysis:
    """
    Performs Exploratory Data Analysis and generates visualizations
    """
    
    def __init__(self, figsize=(15, 10)):
        """
        Initialize EDA
        
        Args:
            figsize: Figure size for plots
        """
        self.figsize = figsize
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = figsize
    
    def generate_basic_statistics(self, df, target_column='Churn'):
        """
        Generate basic statistics
        
        Args:
            df: Input DataFrame
            target_column: Target column name
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'target_distribution': df[target_column].value_counts().to_dict() if target_column in df.columns else None,
            'churn_rate': (df[target_column].sum() / len(df) * 100) if target_column in df.columns else None,
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': len(df) - len(df.drop_duplicates())
        }
        logger.info(f"Statistics: {stats}")
        return stats
    
    def plot_churn_distribution(self, df, target_column='Churn', save_path=None):
        """
        Plot churn distribution
        
        Args:
            df: Input DataFrame
            target_column: Target column name
            save_path: Path to save the plot
        """
        if target_column not in df.columns:
            logger.warning(f"Column {target_column} not found")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Count plot
        churn_counts = df[target_column].value_counts()
        axes[0].bar(churn_counts.index, churn_counts.values, color=['green', 'red'])
        axes[0].set_title('Churn Distribution (Count)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Churn')
        axes[0].set_ylabel('Count')
        
        # Percentage plot
        churn_pct = df[target_column].value_counts(normalize=True) * 100
        axes[1].pie(churn_pct.values, labels=['No Churn', 'Churn'], autopct='%1.1f%%', 
                   colors=['green', 'red'])
        axes[1].set_title('Churn Distribution (Percentage)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        plt.close()
    
    def plot_numerical_distributions(self, df, columns=None, save_path=None):
        """
        Plot distributions of numerical columns
        
        Args:
            df: Input DataFrame
            columns: List of columns to plot (if None, plots all numerical columns)
            save_path: Path to save the plot
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        n_cols = min(len(columns), 4)
        n_rows = (len(columns) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3*n_rows))
        axes = axes.flatten() if len(columns) > 1 else [axes]
        
        for idx, col in enumerate(columns):
            axes[idx].hist(df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
            axes[idx].set_title(f'{col} Distribution', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
        
        # Hide unused subplots
        for idx in range(len(columns), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        plt.close()
    
    def plot_categorical_distributions(self, df, columns=None, save_path=None):
        """
        Plot distributions of categorical columns
        
        Args:
            df: Input DataFrame
            columns: List of columns to plot (if None, plots all categorical columns)
            save_path: Path to save the plot
        """
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns.tolist()
        
        n_cols = min(len(columns), 3)
        n_rows = (len(columns) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
        axes = axes.flatten() if len(columns) > 1 else [axes]
        
        for idx, col in enumerate(columns):
            value_counts = df[col].value_counts()
            axes[idx].barh(value_counts.index, value_counts.values, color='skyblue', edgecolor='black')
            axes[idx].set_title(f'{col} Distribution', fontsize=12, fontweight='bold')
            axes[idx].set_xlabel('Count')
        
        # Hide unused subplots
        for idx in range(len(columns), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        plt.close()
    
    def plot_correlation_matrix(self, df, save_path=None):
        """
        Plot correlation matrix for numerical columns
        
        Args:
            df: Input DataFrame
            save_path: Path to save the plot
        """
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 1:
            corr_matrix = df[numerical_cols].corr()
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, fmt='.2f', cbar_kws={"shrink": 0.8})
            plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Plot saved to {save_path}")
            plt.close()
    
    def plot_confusion_matrix(self, confusion_matrix, save_path=None):
        """
        Plot confusion matrix
        
        Args:
            confusion_matrix: Confusion matrix array
            save_path: Path to save the plot
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Churn', 'Churn'],
                   yticklabels=['No Churn', 'Churn'])
        plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        plt.close()
    
    def generate_eda_report(self, df, target_column='Churn', output_dir='eda_report'):
        """
        Generate complete EDA report with all visualizations
        
        Args:
            df: Input DataFrame
            target_column: Target column name
            output_dir: Directory to save plots
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("Generating EDA report...")
        
        # Basic statistics
        stats = self.generate_basic_statistics(df, target_column)
        
        # Plots
        self.plot_churn_distribution(df, target_column, 
                                     os.path.join(output_dir, 'churn_distribution.png'))
        self.plot_numerical_distributions(df, 
                                         os.path.join(output_dir, 'numerical_distributions.png'))
        self.plot_categorical_distributions(df, 
                                           os.path.join(output_dir, 'categorical_distributions.png'))
        self.plot_correlation_matrix(df, 
                                    os.path.join(output_dir, 'correlation_matrix.png'))
        
        logger.info(f"EDA report generated in {output_dir}")
        return stats
