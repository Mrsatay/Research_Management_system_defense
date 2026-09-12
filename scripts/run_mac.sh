#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

if [ ! -x ".venv/bin/python" ]; then
    echo "Virtual environment not found. Run: python3 -m venv .venv"
    exit 1
fi

".venv/bin/python" "main.py"
