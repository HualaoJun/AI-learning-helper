@echo off
chcp 65001 >nul
title AI Code Learning Assistant
echo ============================================================
echo         AI Code Learning Assistant
echo ============================================================
echo.
echo Starting with python3...
python3 "%~dp0main.py"
if errorlevel 1 (
    echo.
    echo python3 not found, trying python...
    python "%~dp0main.py"
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed or not in PATH.
        echo Please install Python 3.7+ from https://www.python.org/downloads/
        echo.
        pause
    )
)
echo.
echo.
echo Press any key to exit...
pause >nul