#!/usr/bin/env python3
"""
Auto DevOps Assistant - Dependency Installer
Installs all required dependencies for the project.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🤖 Auto DevOps Assistant - Dependency Installer")
    print("=" * 50)
    
    # Core dependencies needed for the application
    dependencies = [
        "Flask==3.1.1",
        "flask-cors==6.0.1", 
        "SQLAlchemy==2.0.35",
        "PyMySQL==1.1.1",
        "Werkzeug==3.1.3",
        "Jinja2==3.1.6"
    ]
    
    print("📦 Installing Python dependencies...")
    print("-" * 30)
    
    failed_packages = []
    
    for package in dependencies:
        print(f"Installing {package}...", end=" ")
        if install_package(package):
            print("✓")
        else:
            print("❌")
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if failed_packages:
        print("❌ Some packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\nTry running manually:")
        print("  pip install Flask flask-cors SQLAlchemy PyMySQL")
        return 1
    
    # Test imports
    print("🔍 Testing imports...")
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
        
        import flask_cors
        print("✓ Flask-CORS")
        
        import sqlalchemy
        print(f"✓ SQLAlchemy {sqlalchemy.__version__}")
        
        import pymysql
        print(f"✓ PyMySQL {pymysql.__version__}")
        
        print("\n🎉 All dependencies installed successfully!")
        print("\n🚀 You can now start the server:")
        print("  cd backend")
        print("  python app.py")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("\nTry reinstalling manually:")
        print("  pip install Flask flask-cors SQLAlchemy PyMySQL")
        return 1

if __name__ == '__main__':
    sys.exit(main())
