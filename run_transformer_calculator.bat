@echo off
cd /d "%~dp0"
rem --- Ensure a virtual environment exists ---
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment in .venv...
    rem Prefer py -3, fall back to python on PATH
    py -3 -m venv .venv 2>nul || python -m venv .venv 2>nul || (
        echo ERROR: No Python 3 found on PATH and no `py` launcher available.
        echo Please install Python 3 and try again.
        pause
        exit /b 1
    )
)

rem --- Activate the virtual environment ---
call ".venv\Scripts\activate"

rem --- Upgrade pip and install requirements if present ---
python -m pip install --upgrade pip >nul 2>&1
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt || (
        echo WARNING: Failed to install some dependencies. Continuing to run the app.
    )
)

rem --- Run the application (forward any arguments) ---
python main.py %*
if errorlevel 1 pause
