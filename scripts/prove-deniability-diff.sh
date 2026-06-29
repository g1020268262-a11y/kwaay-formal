#!/usr/bin/env bash
set -u

OUTDIR="logs/tamarin-deniability"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-300}"
SUMMARY="$OUTDIR/summary.txt"

mkdir -p "$OUTDIR"
: > "$SUMMARY"

run_cmd() {
  local name="$1"
  shift
  local log="$OUTDIR/${name}.out"
  local expected="${EXPECTED_RESULT:-}"

  printf "%-58s" "$name"
  timeout "$TIMEOUT_SECONDS" "$@" > "$log" 2>&1
  local status=$?

  local result="UNKNOWN"
  if [ "$status" -eq 124 ]; then
    result="TIMEOUT"
  elif [ "$status" -eq 0 ] && [ "${name%_parse}" != "$name" ]; then
    result="OK"
  elif grep -q "falsified" "$log"; then
    result="FALSIFIED"
  elif grep -q "verified" "$log"; then
    result="VERIFIED"
  elif grep -q "analysis incomplete" "$log"; then
    result="INCOMPLETE"
  elif [ "$status" -ne 0 ]; then
    result="ERROR"
  fi

  if grep -q "WARNING: [1-9][0-9]* wellformedness check failed" "$log"; then
    result="${result}_WITH_WARNING"
  fi

  if [ "$expected" = "NON_EQUIV" ]; then
    if [ "$result" = "VERIFIED" ] || [ "$result" = "VERIFIED_WITH_WARNING" ]; then
      result="UNEXPECTED_EQUIV"
    elif [ "$result" = "FALSIFIED" ] || [ "$result" = "ERROR" ] || [ "$result" = "INCOMPLETE" ] || [ "$result" = "UNKNOWN" ]; then
      result="EXPECTED_NON_EQUIV"
    fi
  fi

  echo "$result"
  printf "%-70s %s\n" "$name" "$result" >> "$SUMMARY"
}

CORE="tamarin/kwaay_deniability_core_diff.spthy"
MALICIOUS="tamarin/kwaay_deniability_malicious_pok_diff.spthy"
NEGATIVE="tamarin/kwaay_deniability_negative_sender_secret_diff.spthy"

echo "Logs: $OUTDIR"
echo "Timeout per command: ${TIMEOUT_SECONDS}s"
echo

run_cmd core_parse tamarin-prover --diff --parse-only "$CORE"
run_cmd malicious_pok_parse tamarin-prover --diff --parse-only "$MALICIOUS"
run_cmd negative_parse tamarin-prover --diff --parse-only "$NEGATIVE"

run_cmd core_executable_real tamarin-prover --diff --prove=executable_core_real_transcript "$CORE"
run_cmd core_executable_simulated tamarin-prover --diff --prove=executable_core_simulated_transcript "$CORE"

run_cmd malicious_executable_real tamarin-prover --diff --prove=executable_malicious_pok_real_transcript "$MALICIOUS"
run_cmd malicious_executable_simulated tamarin-prover --diff --prove=executable_malicious_pok_simulated_transcript "$MALICIOUS"
run_cmd malicious_registered_witness tamarin-prover --diff --prove=registered_malicious_receiver_has_extracted_witness "$MALICIOUS"
run_cmd malicious_simulator_witness tamarin-prover --diff --prove=simulator_uses_extracted_witness "$MALICIOUS"

run_cmd negative_executable_real tamarin-prover --diff --prove=executable_negative_real_transcript "$NEGATIVE"
run_cmd negative_executable_simulated tamarin-prover --diff --prove=executable_negative_simulated_transcript "$NEGATIVE"

run_cmd core_observational_equivalence tamarin-prover --diff --prove "$CORE"
run_cmd malicious_observational_equivalence tamarin-prover --diff --prove "$MALICIOUS"
EXPECTED_RESULT=NON_EQUIV run_cmd negative_observational_equivalence tamarin-prover --diff --prove "$NEGATIVE"

echo
echo "Deniability proof summary"
cat "$SUMMARY"
