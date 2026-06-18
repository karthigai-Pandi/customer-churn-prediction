"""
Project Setup Verification Script
Checks if all dependencies are installed and project is ready to run
"""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (Need 3.8+)")
        return False

def check_packages():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'sklearn',
        'xgboost',
        'joblib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package:20} installed")
        except ImportError:
            print(f"✗ {package:20} NOT installed")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_directories():
    """Check if required directories exist"""
    directories = [
        'src',
        'templates',
        'static',
        'data',
        'models',
        'documentation'
    ]
    
    all_exist = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory:20} exists")
        else:
            print(f"✗ {directory:20} NOT found")
            all_exist = False
    
    return all_exist

def check_files():
    """Check if required files exist"""
    files = [
        'generate_data.py',
        'run.py',
        'requirements.txt',
        'src/model.py',
        'src/app.py',
        'templates/base.html',
        'templates/login.html',
        'static/style.css'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file:40} exists")
        else:
            print(f"✗ {file:40} NOT found")
            all_exist = False
    
    return all_exist

def check_data():
    """Check if dataset exists"""
    if os.path.exists('data/churn_data.csv'):
        size_mb = os.path.getsize('data/churn_data.csv') / (1024 * 1024)
        print(f"✓ Dataset exists ({size_mb:.2f} MB)")
        return True
    else:
        print("⚠ Dataset not found (run: python generate_data.py)")
        return False

def check_models():
    """Check if trained models exist"""
    models = [
        'models/churn_model.pkl',
        'models/scaler.pkl',
        'models/encoders.pkl',
        'models/features.pkl'
    ]
    
    all_exist = True
    for model in models:
        if os.path.exists(model):
            print(f"✓ {model:40} exists")
        else:
            print(f"⚠ {model:40} not found")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("Customer Churn Prediction - Project Verification")
    print("="*70 + "\n")
    
    print("PYTHON VERSION")
    print("-" * 70)
    python_ok = check_python_version()
    
    print("\nREQUIRED PACKAGES")
    print("-" * 70)
    packages_ok, missing = check_packages()
    
    if not packages_ok:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
    
    print("\nDIRECTORIES")
    print("-" * 70)
    dirs_ok = check_directories()
    
    print("\nFILES")
    print("-" * 70)
    files_ok = check_files()
    
    print("\nDATASET")
    print("-" * 70)
    data_ok = check_data()
    
    print("\nMODELS")
    print("-" * 70)
    models_ok = check_models()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    status = {
        'Python Version': python_ok,
        'Packages': packages_ok,
        'Directories': dirs_ok,
        'Files': files_ok,
        'Dataset': data_ok,
        'Trained Models': models_ok
    }
    
    for check, result in status.items():
        symbol = "✓" if result else "✗"
        print(f"{symbol} {check}")
    
    print("\nNEXT STEPS")
    print("-" * 70)
    
    if not packages_ok:
        print("1. Install dependencies: pip install -r requirements.txt")
    
    if not data_ok:
        print("2. Generate dataset: python generate_data.py")
    
    if not models_ok:
        print("3. Train model: python -m src.model")
    
    print("4. Run application: python run.py")
    print("5. Open browser: http://127.0.0.1:5000")
    
    all_ok = all(status.values())
    
    if all_ok:
        print("\n✓ All checks passed! Project is ready to run.")
        print("Start with: python run.py")
    else:
        print("\n⚠ Some checks failed. Follow the steps above.")
    
    print("="*70 + "\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
