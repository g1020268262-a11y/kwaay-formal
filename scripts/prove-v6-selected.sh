#!/usr/bin/env bash
set -u

FILE="tamarin/kwaay_splitkem_batch_dynamic_v6.spthy"
OUTDIR="logs/tamarin-v6"
TIMEOUT_SECONDS=300
SUMMARY="$OUTDIR/summary.txt"

mkdir -p "$OUTDIR"
: > "$SUMMARY"

LEMMAS=(
  executable_add_slot
  executable_seal_batch
  executable_process_slot
  executable_batch_complete
  executable_batch_fail
  process_requires_slot_added
  process_requires_seal
  complete_requires_seal
  fail_requires_seal
  batch_complete_consumes_state
  batch_fail_consumes_state
  batch_end_token_single_use
  batch_fail_complete_exclusive
  slot_origin_without_early_compromise
  slot_key_known_requires_exception
  partnered_slot_key_not_attacker_known_without_early_compromise
)

echo "Target file: $FILE"
echo "Logs: $OUTDIR"
echo "Timeout per lemma: ${TIMEOUT_SECONDS}s"
echo

for LEMMA in "${LEMMAS[@]}"; do
  LOG="$OUTDIR/${LEMMA}.out"

  echo "============================================================"
  echo "Proving: $LEMMA"
  echo "============================================================"

  timeout "$TIMEOUT_SECONDS" tamarin-prover --prove="$LEMMA" "$FILE" 2>&1 | tee "$LOG"
  STATUS=${PIPESTATUS[0]}

  if [ "$STATUS" -eq 124 ]; then
    RESULT="TIMEOUT"
  elif grep -q "falsified" "$LOG"; then
    RESULT="FALSIFIED"
  elif grep -q "verified" "$LOG"; then
    RESULT="VERIFIED"
  elif grep -q "analysis incomplete" "$LOG"; then
    RESULT="INCOMPLETE"
  else
    RESULT="UNKNOWN"
  fi

  printf "%-70s %s\n" "$LEMMA" "$RESULT" | tee -a "$SUMMARY"
  echo
done

echo "============================================================"
echo "Selected lemma summary"
echo "============================================================"
cat "$SUMMARY"
