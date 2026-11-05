#!/usr/bin/env sh
# Repeatable local equivalent of the checks run before GitHub Pages deployment.
set -eu

if [ -x "./.venv/bin/python" ]; then
  PYTHON="./.venv/bin/python"
else
  PYTHON="${PYTHON:-python3}"
fi

"$PYTHON" -m compileall main.py build_static.py site_content.py utils scripts
"$PYTHON" build_static.py
"$PYTHON" scripts/check_site.py
"$PYTHON" scripts/check_integrity.py
npm run build
