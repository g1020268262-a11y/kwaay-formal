#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="$ROOT_DIR/proverif/kwaay_core_final.cpp.pv"
LOG_ROOT="$ROOT_DIR/logs/final/proverif"
GENERATED_DIR="$LOG_ROOT/generated"
OUT_DIR="$LOG_ROOT/out"
SUMMARY="$LOG_ROOT/summary.txt"
TIMEOUT_SECONDS=300

ALL_TARGETS=(
  BASELINE
  COMPONENT
  EXCEPTION_CHOICE
  RECEIVER_EXCEPTION_CLASSIFICATION
  LEAK_SIGSK_A
  LEAK_SIGSK_B
  LEAK_SIGSK_AB
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

mkdir -p "$GENERATED_DIR" "$OUT_DIR"

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
  echo "THEOREM TARGETS: BASELINE COMPONENT EXCEPTION_CHOICE"
  echo "CLASSIFICATION / EXPERIMENT TARGETS: RECEIVER_EXCEPTION_CLASSIFICATION LEAK_SIGSK_A LEAK_SIGSK_B LEAK_SIGSK_AB LEAK_SIGSK LEAK_KEMSK LEAK_EKEMSK LEAK_RSKEMSK LEAK_SSKEMSK LEAK_KEMSK_EKEMSK LEAK_ALL_RECEIVER_SECRETS"
  echo "NOTE: LEAK_SIGSK is kept as a backward-compatible alias for LEAK_SIGSK_AB. Prefer LEAK_SIGSK_A / LEAK_SIGSK_B / LEAK_SIGSK_AB for new analysis."
  echo
} > "$SUMMARY"

for target in "${TARGETS[@]}"; do
  generated="$GENERATED_DIR/${target}.pv"
  out="$OUT_DIR/${target}.out"
  cpp_err="$OUT_DIR/${target}.cpp.err"

  echo "== $target =="
  echo "TARGET: $target" >> "$SUMMARY"

  cpp -P -D "$target" "$MODEL" > "$generated" 2> "$cpp_err"
  cpp_status=$?
  if [ "$cpp_status" -ne 0 ]; then
    echo "  cpp: FAIL ($cpp_status)"
    echo "STATUS: FAIL" >> "$SUMMARY"
    echo "REASON: cpp_failed($cpp_status)" >> "$SUMMARY"
    echo "OUTPUT: $out" >> "$SUMMARY"
    echo "GENERATED: $generated" >> "$SUMMARY"
    sed 's/^/CPP: /' "$cpp_err" >> "$SUMMARY"
    echo >> "$SUMMARY"
    continue
  fi

  if [ "$PROVERIF_NEEDS_WIN_PATH" -eq 1 ] && command -v wslpath >/dev/null 2>&1; then
    proverif_input="$(wslpath -w "$generated")"
  else
    proverif_input="$generated"
  fi

  if command -v timeout >/dev/null 2>&1; then
    timeout "$TIMEOUT_SECONDS" "${PROVERIF_CMD[@]}" "$proverif_input" > "$out" 2>&1
    pv_status=$?
    if [ "$pv_status" -eq 124 ]; then
      echo "  proverif: TIMEOUT"
      echo "STATUS: TIMEOUT" >> "$SUMMARY"
      echo "OUTPUT: $out" >> "$SUMMARY"
      echo "GENERATED: $generated" >> "$SUMMARY"
      echo >> "$SUMMARY"
      continue
    fi
  else
    "${PROVERIF_CMD[@]}" "$proverif_input" > "$out" 2>&1
    pv_status=$?
  fi

  if [ "$pv_status" -eq 0 ]; then
    echo "  proverif: OK"
    echo "STATUS: OK" >> "$SUMMARY"
  else
    echo "  proverif: FAIL ($pv_status)"
    echo "STATUS: FAIL" >> "$SUMMARY"
    echo "REASON: proverif_failed($pv_status)" >> "$SUMMARY"
  fi

  echo "OUTPUT: $out" >> "$SUMMARY"
  echo "GENERATED: $generated" >> "$SUMMARY"
  if grep -q '^RESULT' "$out"; then
    echo "RESULTS:" >> "$SUMMARY"
    grep '^RESULT' "$out" >> "$SUMMARY"
  else
    echo "RESULTS: none-found" >> "$SUMMARY"
  fi
  echo >> "$SUMMARY"
done

echo
echo "summary: $SUMMARY"
