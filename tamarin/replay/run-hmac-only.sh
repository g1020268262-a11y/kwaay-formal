#!/usr/bin/env bash

set -u
set -o pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODEL_REL="tamarin/replay/kwaay_replay_hmac_only.spthy"
MODEL="$ROOT_DIR/$MODEL_REL"
LOG_DIR="$ROOT_DIR/logs/tamarin-replay-hmac-only"
COMMAND_LOG="$LOG_DIR/command.txt"
VERSIONS_LOG="$LOG_DIR/versions.txt"
RAW_LOG="$LOG_DIR/raw.out"
SUMMARY_LOG="$LOG_DIR/summary.txt"
PARSE_LOG="$LOG_DIR/parse.out"
ATTACK_RAW_LOG="$LOG_DIR/attack-trace.out"
ATTACK_JSON_LOG="$LOG_DIR/attack-trace.json"
ATTACK_DOT_LOG="$LOG_DIR/attack-trace.dot"
if [ -x /mnt/d/Git/cmd/git.exe ] && command -v wslpath >/dev/null 2>&1; then
  GIT_ROOT="$(wslpath -w "$ROOT_DIR")"
  GIT_CMD=(/mnt/d/Git/cmd/git.exe -C "$GIT_ROOT")
else
  GIT_CMD=(git -c "safe.directory=$ROOT_DIR" -C "$ROOT_DIR")
fi

mkdir -p "$LOG_DIR"

{
  echo "repository: $ROOT_DIR"
  echo "model: $MODEL_REL"
  echo "utc: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "git_head: $("${GIT_CMD[@]}" rev-parse HEAD)"
  echo "git_branch: $("${GIT_CMD[@]}" branch --show-current)"
  echo "git_status_short:"
  "${GIT_CMD[@]}" status --short
  echo
  echo "tamarin-prover --version"
  tamarin-prover --version
  echo
  echo "maude --version"
  maude --version
  echo
  echo "proverif -version"
  if command -v proverif >/dev/null 2>&1; then
    proverif -version 2>&1 || true
  elif command -v proverif.exe >/dev/null 2>&1; then
    proverif.exe -version 2>&1 || true
  elif [ -x /mnt/d/Proverif/proverif2.05/proverif.exe ]; then
    /mnt/d/Proverif/proverif2.05/proverif.exe -version 2>&1 || true
  else
    echo "proverif: not found"
  fi
} > "$VERSIONS_LOG" 2>&1

{
  echo "working_directory: $ROOT_DIR"
  echo "parse_command: tamarin-prover --parse-only $MODEL_REL"
  echo "proof_command: tamarin-prover --prove $MODEL_REL"
  echo "trace_command: tamarin-prover --prove=one_confirmed_send_two_accepts_exists --output-json=logs/tamarin-replay-hmac-only/attack-trace.json --output-dot=logs/tamarin-replay-hmac-only/attack-trace.dot $MODEL_REL"
  echo "original_regression_command: tamarin-prover --prove tamarin/replay/kwaay_replay_original.spthy"
  echo "hmac_baseline_regression_command: bash proverif/variants/hmac-confirmation/run-hmac-confirmation.sh HMAC_BASELINE"
  echo "hmac_baseline_regression_execution_root: /tmp/kwaay-m1-hmac-regression-b196fdad (unchanged runner/model copies; repository logs not overwritten)"
} > "$COMMAND_LOG"

if [ "${1:-}" = "--versions-only" ]; then
  exit 0
fi

cd "$ROOT_DIR"
set +e
set +o pipefail
tamarin-prover --parse-only "$MODEL_REL" 2>&1 | tee "$PARSE_LOG"
parse_status=${PIPESTATUS[0]}
set -o pipefail
if [ "$parse_status" -ne 0 ]; then
  exit "$parse_status"
fi
tamarin-prover --prove "$MODEL_REL" 2>&1 | tee "$RAW_LOG"
status=${PIPESTATUS[0]}
if [ "$status" -eq 0 ]; then
  tamarin-prover \
    --prove=one_confirmed_send_two_accepts_exists \
    --output-json="$ATTACK_JSON_LOG" \
    --output-dot="$ATTACK_DOT_LOG" \
    "$MODEL_REL" 2>&1 | tee "$ATTACK_RAW_LOG"
  trace_status=${PIPESTATUS[0]}
else
  trace_status=not_run
fi
set -e

{
  echo "K-Waay HMAC-only replay bridge Tamarin summary"
  echo "model: $MODEL_REL"
  echo "parse_exit_status: $parse_status"
  echo "exit_status: $status"
  echo "attack_trace_exit_status: $trace_status"
  echo
  sed -n '/^summary of summaries:/,/^==============================================================================$/{p}' "$RAW_LOG"
} > "$SUMMARY_LOG"

cat "$SUMMARY_LOG"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi
if [ "$trace_status" != "0" ]; then
  exit "$trace_status"
fi
exit 0
