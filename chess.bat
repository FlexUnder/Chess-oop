@echo off
cd /d %~dp0

if not exist venv (
    echo Can not find virtual environment. Creating...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python main.py

pause
