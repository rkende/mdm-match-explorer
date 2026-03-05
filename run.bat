@echo off
REM IBM MDM Match Decision Explorer - Launch Script for Windows

echo 🔍 Starting IBM MDM Match Decision Explorer...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    echo ✓ Dependencies installed
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Please create one based on .env.example
    echo    Copy .env.example to .env and configure your MDM credentials
    pause
    exit /b 1
)

REM Launch Streamlit app
echo.
echo 🚀 Launching application...
echo    The app will open in your browser at http://localhost:8501
echo.
streamlit run src\app.py

@REM Made with Bob
