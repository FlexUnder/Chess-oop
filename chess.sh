#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Can not find virtual environment. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python3 main.py

read -p "Press any key to continue..."