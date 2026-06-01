@echo off
chcp 65001 >nul
title AI Code Learning Assistant
echo ============================================================
echo         AI Code Learning Assistant
echo ============================================================
echo.
echo [1/2] Installing required packages...
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
if errorlevel 1 (
    pip install requests -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
)
echo.
echo [2/2] Starting application...
python "%~dp0main.py"
echo.
pause