#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="$ROOT_DIR/proverif/kwaay_core_final.pv"
OUT_DIR="$ROOT_DIR/logs/final/proverif"
SUMMARY="$OUT_DIR/summary.txt"

ALL_TARGETS=(
  BASELINE
  COMPONENT
  EXCEPTION_CHOICE
  LEAK_SIGSK
  LEAK_KEMSK
  LEAK_EKEMSK
  LEAK_RSKEMSK
  LEAK_SSKEMSK
  LEAK_KEMSK_EKEMSK
  LEAK_ALL_RECEIVER_SECRETS
)

if [ "$#" -gt 0 ]; then
  TARGETS=("$@")
else
  TARGETS=("${ALL_TARGETS[@]}")
fi

mkdir -p "$OUT_DIR"

PROVERIF_CMD=()
PROVERIF_NEEDS_WIN_PATH=0

if command -v proverif >/dev/null 2>&1; then
  PROVERIF_CMD=("$(command -v proverif)")
elif command -v proverif.exe >/dev/null 2>&1; then
  PROVERIF_CMD=("$(command -v proverif.exe)")
  PROVERIF_NEEDS_WIN_PATH=1
elif [ -x /mnt/d/Proverif/proverif2.05/proverif.exe ]; then
  PROVERIF_CMD=(/mnt/d/Proverif/proverif2.05/proverif.exe)
  PROVERIF_NEEDS_WIN_PATH=1
else
  PROVERIF_CMD=(proverif)
fi

{
  echo "K-Waay ProVerif final model summary"
  echo "model: $MODEL"
  echo "proverif: ${PROVERIF_CMD[*]}"
  echo "generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo
} > "$SUMMARY"

for target in "${TARGETS[@]}"; do
  generated="$OUT_DIR/${target}.pv"
  log="$OUT_DIR/${target}.log"

  echo "== $target =="
  echo "target: $target" >> "$SUMMARY"

  cpp -P -D "$target" "$MODEL" > "$generated" 2> "$OUT_DIR/${target}.cpp.err"
  cpp_status=$?
  if [ "$cpp_status" -ne 0 ]; then
    echo "  cpp: failed ($cpp_status)"
    echo "status: cpp_failed($cpp_status)" >> "$SUMMARY"
    sed 's/^/cpp: /' "$OUT_DIR/${target}.cpp.err" >> "$SUMMARY"
    echo >> "$SUMMARY"
    continue
  fi

  if [ "$PROVERIF_NEEDS_WIN_PATH" -eq 1 ] && command -v wslpath >/dev/null 2>&1; then
    proverif_input="$(wslpath -w "$generated")"
  else
    proverif_input="$generated"
  fi

  "${PROVERIF_CMD[@]}" "$proverif_input" > "$log" 2>&1
  pv_status=$?

  if [ "$pv_status" -eq 0 ]; then
    echo "  proverif: finished"
    echo "status: proverif_finished" >> "$SUMMARY"
  else
    echo "  proverif: failed ($pv_status)"
    echo "status: proverif_failed($pv_status)" >> "$SUMMARY"
  fi

  if grep -q '^RESULT' "$log"; then
    echo "query_results:" >> "$SUMMARY"
    grep '^RESULT' "$log" >> "$SUMMARY"
  else
    echo "query_results: none-found" >> "$SUMMARY"
  fi

  echo "log: $log" >> "$SUMMARY"
  echo "preprocessed: $generated" >> "$SUMMARY"
  echo >> "$SUMMARY"
done

echo
echo "summary: $SUMMARY"
