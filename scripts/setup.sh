#!/usr/bin/env bash
set -e
uv venv .venv

if [[ "$OS" == "Windows_NT" ]]; then
    ACTIVATE=".venv/Scripts/activate"
else
    ACTIVATE=".venv/bin/activate"
fi
source "$ACTIVATE"

export PYTHONPATH=$(pwd)/src

python - <<'PY'
import tomllib, subprocess
with open('pyproject.toml','rb') as f:
    data = tomllib.load(f)
deps = data['project']['dependencies']
dev_deps = data['project']['optional-dependencies']['dev']
subprocess.check_call(['uv','pip','install',*deps])
subprocess.check_call(['uv','pip','install',*dev_deps])
PY

python - <<'PY'
from infrastructure.db import get_engine, init_db
engine = get_engine()
init_db(engine)
PY

