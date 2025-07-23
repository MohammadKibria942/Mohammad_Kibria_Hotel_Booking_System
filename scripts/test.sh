#!/usr/bin/env bash
export PYTHONPATH=$(pwd)/src
set -e

if [[ "$OS" == "Windows_NT" ]]; then
    ACTIVATE=".venv/Scripts/activate"
else
    ACTIVATE=".venv/bin/activate"
fi

source "$ACTIVATE"
pytest --cov=src tests
pyre --noninteractive --search-path $(python - <<'PY'
import site, os
print(os.pathsep.join(site.getsitepackages()))
PY
)
