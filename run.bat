@echo off
REM ============================================================
REM  NutritionAgent – IBM Granite AI  |  run.bat
REM  Double-click to launch the Nutrition Agentic AI app
REM ============================================================

title NutritionAgent – IBM Granite AI

echo.
echo  ============================================================
echo   NutritionAgent – IBM Granite LLM  ^|  Powered by IBM Bob
echo  ============================================================
echo.

REM ── Check Python installation ────────────────────────────────
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python 3.10+ from https://www.python.org/downloads/
    echo  and re-run this script.
    pause
    exit /b 1
)

REM ── Install / upgrade dependencies ───────────────────────────
echo  [SETUP] Installing/verifying dependencies...
python -m pip install -q -r requirements.txt
IF ERRORLEVEL 1 (
    echo  [ERROR] Failed to install requirements.
    echo  Try: python -m pip install -r requirements.txt
    pause
    exit /b 1
)
echo  [SETUP] Dependencies are ready.

REM ── Check .env file ──────────────────────────────────────────
IF NOT EXIST ".env" (
    echo.
    echo  [WARNING] .env file not found!
    echo  Please create a .env file with:
    echo    IBM_API_KEY=your_api_key_here
    echo    IBM_PROJECT_ID=your_project_id_here
    echo    IBM_REGION=https://us-south.ml.cloud.ibm.com
    echo  See README.md for full instructions.
    echo.
    pause
    exit /b 1
)

REM ── Launch application ────────────────────────────────────────
echo.
echo  [INFO] Starting NutritionAgent...
echo  [INFO] Press Ctrl+C at any time to exit.
echo.

python main.py

echo.
echo  ============================================================
echo   Session ended. Your nutrition plan is saved in:
echo   nutrition_plans\
echo  ============================================================
pause
