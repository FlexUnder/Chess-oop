@echo off
cd /d %~dp0

if not exist venv (
    echo Виртуальное окружение не найдено. Создание...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python main.py

pause
