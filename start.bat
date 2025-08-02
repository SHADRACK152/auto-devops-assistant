@echo off
echo.
echo ========================================
echo Auto DevOps Assistant - TiDB AgentX Hackathon
echo ========================================
echo.

echo Checking and activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo Virtual environment not found, using global Python...
)

echo.
echo Installing/checking dependencies...
python -m pip install Flask flask-cors SQLAlchemy PyMySQL --quiet

echo.
echo Starting Auto DevOps Assistant server...
echo.
echo Server will be available at:
echo   Frontend: http://127.0.0.1:5000/
echo   Health: http://127.0.0.1:5000/health
echo.

cd /d "%~dp0backend"
python app.py

echo.
echo Server stopped.
pause
