#!/usr/bin/env bash
set -u

FILE="tamarin/kwaay_splitkem_batch_dynamic_v7.spthy"
OUTDIR="logs/tamarin-v7"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-300}"
SUMMARY="$OUTDIR/summary.txt"

mkdir -p "$OUTDIR"
: > "$SUMMARY"

LEMMAS=(
  executable_four_slots_added
  executable_seal_batch
  executable_four_slots_processed
  executable_batch_complete
  executable_batch_fail
  seal_requires_all_slots_added
  process_requires_slot_added
  process_requires_seal
  complete_requires_seal
  fail_requires_seal
  complete_requires_all_slots_done
  complete_requires_all_added_slots_processed
  no_add_after_seal
  no_add_after_complete
  no_add_after_fail
  no_slot_accept_after_complete
  no_slot_accept_after_fail
  no_slot_accept_after_close
  batch_complete_consumes_state
  batch_fail_consumes_state
  batch_end_token_single_use
  batch_fail_complete_exclusive
  receiver_state_single_batch_end
  slot_origin
)

echo "Target file: $FILE"
echo "Logs: $OUTDIR"
echo "Timeout per lemma: ${TIMEOUT_SECONDS}s"
echo

for LEMMA in "${LEMMAS[@]}"; do
  LOG="$OUTDIR/${LEMMA}.out"

  printf "%-58s" "$LEMMA"

  timeout "$TIMEOUT_SECONDS" tamarin-prover --prove="$LEMMA" "$FILE" > "$LOG" 2>&1
  STATUS=$?

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

  echo "$RESULT"
  printf "%-70s %s\n" "$LEMMA" "$RESULT" >> "$SUMMARY"
done

echo
echo "Selected lemma summary"
cat "$SUMMARY"
