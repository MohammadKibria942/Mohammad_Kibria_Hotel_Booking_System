#!/usr/bin/env bash
export PYTHONPATH=$(pwd)/src
set -e

if [[ "$OS" == "Windows_NT" ]]; then
    ACTIVATE=".venv/Scripts/activate"
else
    ACTIVATE=".venv/bin/activate"
fi
source "$ACTIVATE"

uvicorn src.api.main:app --host 0.0.0.0 --port 8000
