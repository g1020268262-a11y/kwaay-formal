#!/usr/bin/env bash
set -euo pipefail

RUNNER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT_DIR="$(cd "$RUNNER_DIR/.." && pwd -P)"
if [[ ! -v PYTHON_CMD && -n "${WSL_INTEROP:-}" ]] && command -v python.exe >/dev/null 2>&1; then
  PYTHON_CMD=python.exe
else
  PYTHON_CMD="${PYTHON_CMD:-python3}"
fi
if [[ -n "${WSL_INTEROP:-}" && "$PYTHON_CMD" == *.exe ]] && command -v wslpath >/dev/null 2>&1; then
  ROOT_DIR="$(wslpath -w "$ROOT_DIR")"
fi
export PYTHONDONTWRITEBYTECODE=1

usage() {
  cat <<'EOF'
usage: scripts/run-paper-artifact.sh [MODE] [OPTIONS]

Modes:
  verify-committed  validate committed blobs/evidence without a prover (default)
  list              list modes and scope
  smoke             small check, not a full reproduction; requires --output
  paper-core        selected paper-core targets; requires --output
  m4-tamarin        296 Tamarin targets; requires --output
  full              all direct expected properties; requires --output
  assemble-only     validate/combine two complete runs; requires --mode,
                    --run1, --run2, and --output
EOF
}

mode="${1:-verify-committed}"
if [[ $# -gt 0 ]]; then shift; fi
case "$mode" in
  verify-committed)
    [[ $# -eq 0 ]] || { usage >&2; exit 2; }
    exec "$PYTHON_CMD" -B "$ROOT_DIR/scripts/artifact/verify_contract.py"
    ;;
  list)
    [[ $# -eq 0 ]] || { usage >&2; exit 2; }
    usage
    ;;
  smoke|paper-core|m4-tamarin|full|assemble-only)
    exec "$PYTHON_CMD" -B "$ROOT_DIR/scripts/artifact/run_modes.py" "$mode" "$@"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "error: unknown mode: $mode" >&2
    usage >&2
    exit 2
    ;;
esac
