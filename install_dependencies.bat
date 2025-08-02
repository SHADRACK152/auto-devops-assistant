@echo off
echo ========================================
echo Installing Auto DevOps Assistant Dependencies
echo ========================================
echo.

echo Activating virtual environment...
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Virtual environment created and activated!
)

echo.
echo Installing dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install Flask==3.1.1
python -m pip install flask-cors==6.0.1
python -m pip install SQLAlchemy==2.0.35
python -m pip install PyMySQL==1.1.1

echo.
echo Testing installation...
python -c "import flask; import flask_cors; import sqlalchemy; import pymysql; print('✓ All dependencies installed successfully!')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start the server:
echo   1. Make sure you're in the backend directory
echo   2. Run: python app.py
echo.
pause
