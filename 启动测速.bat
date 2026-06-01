@echo off
chcp 65001 >nul
title WiFi 网速测试
cd /d "%~dp0"

if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -q
python main.py
pause
