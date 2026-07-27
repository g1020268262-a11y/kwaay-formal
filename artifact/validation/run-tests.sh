#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
if [[ ! -v PYTHON_CMD && -n "${WSL_INTEROP:-}" ]] && command -v python.exe >/dev/null 2>&1; then
  PYTHON_CMD=python.exe
else
  PYTHON_CMD="${PYTHON_CMD:-python3}"
fi
if [[ -n "${WSL_INTEROP:-}" && "$PYTHON_CMD" == *.exe ]] && command -v wslpath >/dev/null 2>&1; then
  ROOT_DIR="$(wslpath -w "$ROOT_DIR")"
fi
export PYTHONDONTWRITEBYTECODE=1

"$PYTHON_CMD" -B "$ROOT_DIR/artifact/validation/test_contract.py"
