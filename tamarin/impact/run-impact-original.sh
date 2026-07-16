#!/usr/bin/env bash

set -euo pipefail

if [[ -n "${KWAAY_REPO_ROOT+x}" ]]; then
  echo "error: KWAAY_REPO_ROOT is not accepted; the runner derives its repository from its own path" >&2
  exit 2
fi

RUNNER_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
RUNNER_DIR="$(dirname "$RUNNER_PATH")"
ROOT_DIR="$(cd "$RUNNER_DIR/../.." && pwd -P)"

MODEL_REL="tamarin/impact/kwaay_impact_original.spthy"
RUNNER_REL="tamarin/impact/run-impact-original.sh"
ORIGINAL_REL="tamarin/replay/kwaay_replay_original.spthy"
LOG_REL="logs/tamarin-impact-original"

MODEL="$ROOT_DIR/$MODEL_REL"
ORIGINAL_MODEL="$ROOT_DIR/$ORIGINAL_REL"
LOG_DIR="$ROOT_DIR/$LOG_REL"

COMMAND_LOG="$LOG_DIR/command.txt"
VERSIONS_LOG="$LOG_DIR/versions.txt"
PARSE_LOG="$LOG_DIR/parse.out"
RAW_LOG="$LOG_DIR/raw.out"
SUMMARY_LOG="$LOG_DIR/summary.txt"
ATTACK_RAW_LOG="$LOG_DIR/attack-trace.out"
ATTACK_JSON_LOG="$LOG_DIR/attack-trace.json"
ATTACK_DOT_LOG="$LOG_DIR/attack-trace.dot"
UNIQUE_RAW_LOG="$LOG_DIR/unique-install-trace.out"
UNIQUE_JSON_LOG="$LOG_DIR/unique-install-trace.json"
UNIQUE_DOT_LOG="$LOG_DIR/unique-install-trace.dot"
ORIGINAL_RAW_LOG="$LOG_DIR/original-regression.out"
ORIGINAL_SUMMARY_LOG="$LOG_DIR/original-regression-summary.txt"
FORMULA_COMPARISON_LOG="$LOG_DIR/frozen-formula-comparison.txt"
RESULT_COMPARISON_LOG="$LOG_DIR/lower-layer-result-comparison.txt"
MANIFEST_LOG="$LOG_DIR/SHA256SUMS.txt"

if [[ "$RUNNER_PATH" != "$ROOT_DIR/$RUNNER_REL" ]]; then
  echo "error: resolved runner path is outside the expected repository location: $RUNNER_PATH" >&2
  exit 2
fi

if [[ ! -f "$MODEL" || ! -f "$ORIGINAL_MODEL" ]]; then
  echo "error: model file missing" >&2
  exit 2
fi

# Use the repository's Windows Git for the normal /mnt/<drive> checkout, but
# retain Linux Git support for an isolated /tmp clone used by non-formal tests.
if [[ "$ROOT_DIR" == /mnt/?/* ]] \
    && [[ -x /mnt/d/Git/cmd/git.exe ]] \
    && command -v wslpath >/dev/null 2>&1; then
  GIT_ROOT="$(wslpath -w "$ROOT_DIR")"
  GIT_CMD=(/mnt/d/Git/cmd/git.exe -C "$GIT_ROOT")
  REPORTED_GIT_ROOT="$(wslpath -u "$("${GIT_CMD[@]}" rev-parse --show-toplevel)")"
else
  GIT_CMD=(git -c "safe.directory=$ROOT_DIR" -C "$ROOT_DIR")
  REPORTED_GIT_ROOT="$("${GIT_CMD[@]}" rev-parse --show-toplevel)"
fi

if [[ "$(readlink -f "$REPORTED_GIT_ROOT")" != "$ROOT_DIR" ]]; then
  echo "error: runner-derived root and Git root differ" >&2
  exit 2
fi

GIT_HEAD="$("${GIT_CMD[@]}" rev-parse HEAD)"
GIT_TREE="$("${GIT_CMD[@]}" show -s --format=%T HEAD)"
GIT_BRANCH="$("${GIT_CMD[@]}" branch --show-current)"
PRE_RUN_GIT_STATUS="$("${GIT_CMD[@]}" status --porcelain=v1 --untracked-files=all)"

if [[ -n "$PRE_RUN_GIT_STATUS" ]]; then
  echo "error: pre-run git status is not clean" >&2
  printf '%s\n' "$PRE_RUN_GIT_STATUS" >&2
  exit 2
fi

if [[ -e "$LOG_DIR" ]]; then
  echo "error: evidence directory already exists: $LOG_DIR" >&2
  exit 2
fi

for tracked in "$MODEL_REL" "$RUNNER_REL" "$ORIGINAL_REL"; do
  if ! "${GIT_CMD[@]}" cat-file -e "$GIT_HEAD:$tracked" 2>/dev/null; then
    echo "error: $tracked is not tracked by current HEAD" >&2
    exit 2
  fi
done

if ! "${GIT_CMD[@]}" diff --quiet HEAD -- "$MODEL_REL" "$RUNNER_REL" "$ORIGINAL_REL"; then
  echo "error: model, runner, or frozen original model differs from current HEAD" >&2
  exit 2
fi

if [[ -n "$("${GIT_CMD[@]}" status --porcelain=v1 -- "$ORIGINAL_REL")" ]]; then
  echo "error: frozen original model has a worktree modification" >&2
  exit 2
fi

if ! command -v tamarin-prover >/dev/null 2>&1; then
  echo "error: tamarin-prover not found" >&2
  exit 2
fi
if ! command -v maude >/dev/null 2>&1; then
  echo "error: maude not found" >&2
  exit 2
fi

TAMARIN_HELP="$(tamarin-prover --help 2>&1)"
for option in --output-json --output-dot; do
  if ! grep -q -- "$option" <<<"$TAMARIN_HELP"; then
    echo "error: installed Tamarin does not advertise $option" >&2
    exit 2
  fi
done

detect_eol() {
  local file="$1"
  if LC_ALL=C grep -q $'\r$' "$file"; then
    if LC_ALL=C grep -qv $'\r$' "$file"; then
      printf 'mixed-or-CRLF\n'
    else
      printf 'CRLF\n'
    fi
  else
    printf 'LF\n'
  fi
}

MODEL_BLOB_OID="$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$MODEL_REL")"
RUNNER_BLOB_OID="$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$RUNNER_REL")"
ORIGINAL_BLOB_OID="$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$ORIGINAL_REL")"
MODEL_SHA256="$(sha256sum "$MODEL" | awk '{print $1}')"
RUNNER_SHA256="$(sha256sum "$RUNNER_PATH" | awk '{print $1}')"
ORIGINAL_SHA256="$(sha256sum "$ORIGINAL_MODEL" | awk '{print $1}')"
MODEL_EOL="$(detect_eol "$MODEL")"
RUNNER_EOL="$(detect_eol "$RUNNER_PATH")"
ORIGINAL_EOL="$(detect_eol "$ORIGINAL_MODEL")"
GIT_ATTR_OUTPUT="$("${GIT_CMD[@]}" check-attr text eol -- "$MODEL_REL" "$RUNNER_REL" "$ORIGINAL_REL")"

PARSE_CMD=(tamarin-prover --parse-only "$MODEL_REL")
PROOF_CMD=(tamarin-prover --derivcheck-timeout=0 --prove "$MODEL_REL")
ATTACK_CMD=(
  tamarin-prover
  --derivcheck-timeout=0
  --prove=one_send_two_accepts_two_installs_exists
  --output-json="$LOG_REL/attack-trace.json"
  --output-dot="$LOG_REL/attack-trace.dot"
  "$MODEL_REL"
)
UNIQUE_CMD=(
  tamarin-prover
  --derivcheck-timeout=0
  --prove=unique_install_within_completed_consumer
  --output-json="$LOG_REL/unique-install-trace.json"
  --output-dot="$LOG_REL/unique-install-trace.dot"
  "$MODEL_REL"
)
ORIGINAL_CMD=(tamarin-prover --derivcheck-timeout=0 --prove "$ORIGINAL_REL")

COMPOSITION_VERIFIED=(
  accept_output_has_same_time_accept
  receiver_accept_has_output
  receiver_accept_has_unique_output
  accept_id_unique
  install_has_prior_accept
  install_session_has_interface_origin
  install_from_accept_has_session
  install_event_has_single_source
  install_handle_unique
  accept_output_installed_at_most_once
  distinct_accept_sources_have_distinct_handles
  install_requires_batch_complete
  consumer_complete_requires_all_outputs_installed
  consumer_complete_single_use
  no_install_after_consumer_close
  normal_one_accept_one_install
  normal_consumer_complete
  one_send_two_accepts_two_installs_exists
)

FROZEN_LEMMAS=(
  normal_single_accept
  normal_batch_complete
  one_send_two_accepts_exists
  same_message_accepted_at_most_once
  full_message_unique_send
  receiver_accept_has_sender
  injective_receiver_accept
  slot_indices_distinct
  process_requires_slot_added
  process_requires_seal
  complete_requires_all_slots_processed
  no_add_after_seal
  no_accept_after_close
  batch_complete_consumes_state
  batch_fail_consumes_state
  batch_end_token_single_use
  receiver_state_single_batch
  receiver_state_single_batch_end
)

IMPACT_LEMMAS=(
  "${COMPOSITION_VERIFIED[@]}"
  unique_install_within_completed_consumer
  "${FROZEN_LEMMAS[@]}"
)

declare -A IMPACT_EXPECTED_STATUS=()
declare -A ORIGINAL_EXPECTED_STATUS=()
for lemma in "${COMPOSITION_VERIFIED[@]}"; do
  IMPACT_EXPECTED_STATUS["$lemma"]="verified"
done
IMPACT_EXPECTED_STATUS[unique_install_within_completed_consumer]="falsified"
for lemma in "${FROZEN_LEMMAS[@]}"; do
  case "$lemma" in
    same_message_accepted_at_most_once|injective_receiver_accept)
      IMPACT_EXPECTED_STATUS["$lemma"]="falsified"
      ORIGINAL_EXPECTED_STATUS["$lemma"]="falsified"
      ;;
    *)
      IMPACT_EXPECTED_STATUS["$lemma"]="verified"
      ORIGINAL_EXPECTED_STATUS["$lemma"]="verified"
      ;;
  esac
done

print_command() {
  local label="$1"
  shift
  printf '%s:' "$label"
  printf ' %q' "$@"
  printf '\n'
}

run_logged() {
  local output="$1"
  shift
  set +e
  "$@" 2>&1 | tee "$output"
  local status=${PIPESTATUS[0]}
  set -e
  return "$status"
}

extract_summary() {
  local source="$1"
  if [[ -s "$source" ]]; then
    sed -n '/^summary of summaries:/,/^==============================================================================$/{p}' "$source"
  fi
}

# Output columns: lemma, terminal status, steps, raw result text.  A result that
# does not match Tamarin's verified/falsified terminal syntax is nonterminal.
extract_result_rows() {
  local source="$1"
  awk '
    /^summary of summaries:[[:space:]]*$/ { in_summary=1; next }
    in_summary && /^  [[:alnum:]_]+ \((all-traces|exists-trace)\): / {
      line=$0
      sub(/\r$/, "", line)
      name=line
      sub(/^  /, "", name)
      sub(/ .*/, "", name)
      detail=line
      sub(/^.*: /, "", detail)
      status="nonterminal"
      steps="-"
      if (line ~ /: verified \([0-9]+ steps\)$/) {
        status="verified"
        steps=line
        sub(/^.*\(/, "", steps)
        sub(/ steps\)$/, "", steps)
      } else if (line ~ /: falsified - found trace \([0-9]+ steps\)$/) {
        status="falsified"
        steps=line
        sub(/^.*\(/, "", steps)
        sub(/ steps\)$/, "", steps)
      }
      gsub(/\t/, " ", detail)
      print name "\t" status "\t" steps "\t" detail
    }
  ' "$source"
}

validate_exact_results() {
  local rows_file="$1"
  local expected_names_var="$2"
  local expected_status_var="$3"
  local label="$4"
  local -n expected_names_ref="$expected_names_var"
  local -n expected_status_ref="$expected_status_var"
  local errors=0
  local name status steps detail
  declare -A expected_set=()
  declare -A seen=()

  for name in "${expected_names_ref[@]}"; do
    expected_set["$name"]=1
  done

  if [[ ! -s "$rows_file" ]]; then
    echo "error: $label has no mechanically extractable summary rows" >&2
    return 1
  fi

  while IFS=$'\t' read -r name status steps detail; do
    [[ -n "$name" ]] || continue
    if [[ -n "${seen[$name]+x}" ]]; then
      echo "error: $label contains duplicate lemma result: $name" >&2
      errors=1
    fi
    seen["$name"]=1
    if [[ -z "${expected_set[$name]+x}" ]]; then
      echo "error: $label contains unexpected lemma result: $name" >&2
      errors=1
      continue
    fi
    if [[ "$status" != "verified" && "$status" != "falsified" ]]; then
      echo "error: $label lemma is not terminal: $name ($detail)" >&2
      errors=1
    elif [[ "$status" != "${expected_status_ref[$name]}" ]]; then
      echo "error: $label lemma status mismatch: $name actual=$status expected=${expected_status_ref[$name]}" >&2
      errors=1
    fi
  done < "$rows_file"

  for name in "${expected_names_ref[@]}"; do
    if [[ -z "${seen[$name]+x}" ]]; then
      echo "error: $label is missing lemma result: $name" >&2
      errors=1
    fi
  done

  if [[ "${#seen[@]}" -ne "${#expected_names_ref[@]}" ]]; then
    echo "error: $label lemma count mismatch: actual=${#seen[@]} expected=${#expected_names_ref[@]}" >&2
    errors=1
  fi

  return "$errors"
}

extract_lemma_formula_block() {
  local source="$1"
  local lemma_name="$2"
  local destination="$3"
  awk -v target="$lemma_name" '
    { sub(/\r$/, "") }
    $0 == "lemma " target ":" { found=1 }
    found {
      print
      if ($0 ~ /^[[:space:]]*"/) {
        in_formula=1
      }
      if (in_formula && $0 ~ /"[[:space:]]*$/) {
        closed=1
        exit
      }
    }
    END {
      if (!found || !closed) {
        exit 1
      }
    }
  ' "$source" > "$destination"
}

compare_frozen_formulas() {
  local output="$1"
  local tmp_dir="$2"
  local errors=0
  local lemma original_block impact_block original_hash impact_hash comparison
  : > "$output"
  for lemma in "${FROZEN_LEMMAS[@]}"; do
    original_block="$tmp_dir/original-formula-$lemma.txt"
    impact_block="$tmp_dir/impact-formula-$lemma.txt"
    original_hash="EXTRACTION_ERROR"
    impact_hash="EXTRACTION_ERROR"
    comparison="EXTRACTION_ERROR"
    if extract_lemma_formula_block "$ORIGINAL_MODEL" "$lemma" "$original_block"; then
      original_hash="$(sha256sum "$original_block" | awk '{print $1}')"
    else
      errors=1
    fi
    if extract_lemma_formula_block "$MODEL" "$lemma" "$impact_block"; then
      impact_hash="$(sha256sum "$impact_block" | awk '{print $1}')"
    else
      errors=1
    fi
    if [[ "$original_hash" != "EXTRACTION_ERROR" && "$impact_hash" != "EXTRACTION_ERROR" ]]; then
      if cmp -s "$original_block" "$impact_block"; then
        comparison="MATCH"
      else
        comparison="MISMATCH"
        errors=1
      fi
    fi
    {
      echo "lemma: $lemma"
      echo "original_extracted_block_sha256: $original_hash"
      echo "impact_extracted_block_sha256: $impact_hash"
      echo "comparison_result: $comparison"
      echo
    } >> "$output"
  done
  return "$errors"
}

lookup_status() {
  local rows_file="$1"
  local lemma_name="$2"
  awk -F '\t' -v target="$lemma_name" '$1 == target { print $2; found=1 } END { if (!found) exit 1 }' "$rows_file"
}

compare_lower_results() {
  local impact_rows="$1"
  local original_rows="$2"
  local output="$3"
  local errors=0
  local lemma impact_status original_status match
  printf 'lemma\timpact_status\toriginal_status\tmatch\n' > "$output"
  for lemma in "${FROZEN_LEMMAS[@]}"; do
    impact_status="$(lookup_status "$impact_rows" "$lemma" 2>/dev/null || printf 'MISSING')"
    original_status="$(lookup_status "$original_rows" "$lemma" 2>/dev/null || printf 'MISSING')"
    if [[ "$impact_status" == "$original_status" && "$impact_status" != "MISSING" ]]; then
      match="MATCH"
    else
      match="MISMATCH"
      errors=1
    fi
    printf '%s\t%s\t%s\t%s\n' "$lemma" "$impact_status" "$original_status" "$match" >> "$output"
  done
  return "$errors"
}

check_wellformedness_success() {
  local file="$1"
  local label="$2"
  local errors=0

  if [[ ! -s "$file" ]]; then
    echo "error: $label wellformedness output is missing or empty: $file" >&2
    return 1
  fi

  if ! awk '
      { sub(/\r$/, "") }
      $0 == "/* All wellformedness checks were successful. */" { found=1 }
      END { exit(found ? 0 : 1) }
    ' "$file"; then
    echo "error: $label does not contain Tamarin 1.12.0's wellformedness-success marker" >&2
    errors=1
  fi

  if grep -Eiq \
      'WARNING:.*wellformedness|wellformedness.*(warning|errors?|failed)|Wellformedness-error' \
      "$file"; then
    echo "error: $label contains a Tamarin wellformedness warning or error marker" >&2
    errors=1
  fi

  return "$errors"
}

check_trace_artifacts() {
  local label="$1"
  local lemma_name="$2"
  local expected_status="$3"
  local raw_file="$4"
  local json_file="$5"
  local dot_file="$6"
  local rows_file="$7"
  local errors=0
  local actual_status terminal_count

  for artifact in "$raw_file" "$json_file" "$dot_file"; do
    if [[ ! -s "$artifact" ]]; then
      echo "error: $label trace artifact is missing or empty: $artifact" >&2
      errors=1
    fi
  done
  if [[ "$errors" -ne 0 ]]; then
    return 1
  fi

  extract_result_rows "$raw_file" > "$rows_file"
  actual_status="$(lookup_status "$rows_file" "$lemma_name" 2>/dev/null || printf 'MISSING')"
  terminal_count="$(awk -F '\t' '$2 == "verified" || $2 == "falsified" { count++ } END { print count+0 }' "$rows_file")"
  if [[ "$actual_status" != "$expected_status" ]]; then
    echo "error: $label target status mismatch: $lemma_name actual=$actual_status expected=$expected_status" >&2
    errors=1
  fi
  if [[ "$terminal_count" -ne 1 ]]; then
    echo "error: $label trace output has $terminal_count terminal lemmas; expected exactly the selected lemma" >&2
    errors=1
  fi
  for artifact in "$raw_file" "$json_file" "$dot_file"; do
    if ! grep -Fq -- "$lemma_name" "$artifact"; then
      echo "error: $label trace artifact does not identify $lemma_name: $artifact" >&2
      errors=1
    fi
  done
  if [[ "$expected_status" == "falsified" ]] \
      && ! grep -Eq "^  ${lemma_name} \(all-traces\): falsified - found trace \([0-9]+ steps\)\r?$" "$raw_file"; then
    echo "error: $label raw output does not report a counterexample terminal for $lemma_name" >&2
    errors=1
  fi
  if [[ "$expected_status" == "verified" ]] \
      && ! grep -Eq "^  ${lemma_name} \(exists-trace\): verified \([0-9]+ steps\)\r?$" "$raw_file"; then
    echo "error: $label raw output does not report a reachable verified witness for $lemma_name" >&2
    errors=1
  fi
  return "$errors"
}

mkdir -p "$LOG_DIR"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "working_directory: $ROOT_DIR"
  print_command parse_command "${PARSE_CMD[@]}"
  print_command proof_command "${PROOF_CMD[@]}"
  print_command positive_witness_command "${ATTACK_CMD[@]}"
  print_command negative_property_command "${UNIQUE_CMD[@]}"
  print_command original_regression_command "${ORIGINAL_CMD[@]}"
} > "$COMMAND_LOG"

{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "utc_start: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "git_branch: $GIT_BRANCH"
  echo "git_head: $GIT_HEAD"
  echo "git_tree: $GIT_TREE"
  echo "clean_pre_run_status: true"
  echo "pre_run_git_status:"
  printf '%s' "$PRE_RUN_GIT_STATUS"
  echo
  echo "model_git_blob_oid: $MODEL_BLOB_OID"
  echo "model_worktree_sha256: $MODEL_SHA256"
  echo "model_eol: $MODEL_EOL"
  echo "runner_git_blob_oid: $RUNNER_BLOB_OID"
  echo "runner_worktree_sha256: $RUNNER_SHA256"
  echo "runner_eol: $RUNNER_EOL"
  echo "original_model_git_blob_oid: $ORIGINAL_BLOB_OID"
  echo "original_model_worktree_sha256: $ORIGINAL_SHA256"
  echo "original_model_eol: $ORIGINAL_EOL"
  echo "git_check_attr_output:"
  printf '%s\n' "$GIT_ATTR_OUTPUT"
  echo
  echo "tamarin-prover --version:"
  tamarin-prover --version
  echo
  echo "maude --version:"
  maude --version
} > "$VERSIONS_LOG" 2>&1

formula_comparison_status=0
if ! compare_frozen_formulas "$FORMULA_COMPARISON_LOG" "$TMP_DIR"; then
  formula_comparison_status=1
fi

cd "$ROOT_DIR"

parse_status=not_run
proof_status=not_run
attack_status=not_run
unique_status=not_run
original_status=not_run

if run_logged "$PARSE_LOG" "${PARSE_CMD[@]}"; then
  parse_status=0
else
  parse_status=$?
fi

if [[ "$parse_status" -eq 0 ]]; then
  if run_logged "$RAW_LOG" "${PROOF_CMD[@]}"; then
    proof_status=0
  else
    proof_status=$?
  fi
  if run_logged "$ATTACK_RAW_LOG" "${ATTACK_CMD[@]}"; then
    attack_status=0
  else
    attack_status=$?
  fi
  if run_logged "$UNIQUE_RAW_LOG" "${UNIQUE_CMD[@]}"; then
    unique_status=0
  else
    unique_status=$?
  fi
fi

if run_logged "$ORIGINAL_RAW_LOG" "${ORIGINAL_CMD[@]}"; then
  original_status=0
else
  original_status=$?
fi

impact_wellformedness_status=0
if ! check_wellformedness_success "$RAW_LOG" "impact full proof"; then
  impact_wellformedness_status=1
fi

positive_trace_wellformedness_status=0
if ! check_wellformedness_success "$ATTACK_RAW_LOG" "positive witness trace"; then
  positive_trace_wellformedness_status=1
fi

negative_trace_wellformedness_status=0
if ! check_wellformedness_success "$UNIQUE_RAW_LOG" "negative property trace"; then
  negative_trace_wellformedness_status=1
fi

original_wellformedness_status=0
if ! check_wellformedness_success "$ORIGINAL_RAW_LOG" "frozen original proof"; then
  original_wellformedness_status=1
fi

IMPACT_ROWS="$TMP_DIR/impact-results.tsv"
ORIGINAL_ROWS="$TMP_DIR/original-results.tsv"
ATTACK_ROWS="$TMP_DIR/attack-results.tsv"
UNIQUE_ROWS="$TMP_DIR/unique-results.tsv"
: > "$IMPACT_ROWS"
: > "$ORIGINAL_ROWS"
[[ -s "$RAW_LOG" ]] && extract_result_rows "$RAW_LOG" > "$IMPACT_ROWS"
[[ -s "$ORIGINAL_RAW_LOG" ]] && extract_result_rows "$ORIGINAL_RAW_LOG" > "$ORIGINAL_ROWS"

impact_result_validation_status=0
if [[ "$proof_status" != "0" ]] \
    || ! validate_exact_results "$IMPACT_ROWS" IMPACT_LEMMAS IMPACT_EXPECTED_STATUS "impact full proof"; then
  impact_result_validation_status=1
fi

original_result_validation_status=0
if [[ "$original_status" != "0" ]] \
    || ! validate_exact_results "$ORIGINAL_ROWS" FROZEN_LEMMAS ORIGINAL_EXPECTED_STATUS "frozen original proof"; then
  original_result_validation_status=1
fi

attack_artifact_validation_status=0
if [[ "$attack_status" != "0" ]] \
    || ! check_trace_artifacts \
      "positive witness" \
      one_send_two_accepts_two_installs_exists \
      verified \
      "$ATTACK_RAW_LOG" "$ATTACK_JSON_LOG" "$ATTACK_DOT_LOG" "$ATTACK_ROWS"; then
  attack_artifact_validation_status=1
fi

unique_artifact_validation_status=0
if [[ "$unique_status" != "0" ]] \
    || ! check_trace_artifacts \
      "negative property" \
      unique_install_within_completed_consumer \
      falsified \
      "$UNIQUE_RAW_LOG" "$UNIQUE_JSON_LOG" "$UNIQUE_DOT_LOG" "$UNIQUE_ROWS"; then
  unique_artifact_validation_status=1
fi

lower_result_comparison_status=0
if ! compare_lower_results "$IMPACT_ROWS" "$ORIGINAL_ROWS" "$RESULT_COMPARISON_LOG"; then
  lower_result_comparison_status=1
fi

{
  echo "K-Waay M2 original impact/composition Tamarin summary"
  echo "model: $MODEL_REL"
  echo "execution_git_head: $GIT_HEAD"
  echo "execution_git_tree: $GIT_TREE"
  echo "model_git_blob_oid: $MODEL_BLOB_OID"
  echo "runner_git_blob_oid: $RUNNER_BLOB_OID"
  echo "parse_exit_status: $parse_status"
  echo "proof_exit_status: $proof_status"
  echo "positive_witness_exit_status: $attack_status"
  echo "negative_property_exit_status: $unique_status"
  echo "original_regression_exit_status: $original_status"
  echo
  echo "mechanically extracted full proof result table:"
  printf 'lemma\tstatus\tsteps\traw_result\n'
  cat "$IMPACT_ROWS"
  echo
  echo "full proof summary:"
  extract_summary "$RAW_LOG"
  echo
  echo "positive witness export summary:"
  extract_summary "$ATTACK_RAW_LOG"
  echo
  echo "negative property export summary:"
  extract_summary "$UNIQUE_RAW_LOG"
} > "$SUMMARY_LOG"

{
  echo "K-Waay frozen original replay regression summary"
  echo "model: $ORIGINAL_REL"
  echo "execution_git_head: $GIT_HEAD"
  echo "exit_status: $original_status"
  echo
  echo "mechanically extracted result table:"
  printf 'lemma\tstatus\tsteps\traw_result\n'
  cat "$ORIGINAL_ROWS"
  echo
  extract_summary "$ORIGINAL_RAW_LOG"
} > "$ORIGINAL_SUMMARY_LOG"

POST_RUN_GIT_STATUS="$("${GIT_CMD[@]}" status --porcelain=v1 --untracked-files=all)"
UNEXPECTED_STATUS="$(printf '%s\n' "$POST_RUN_GIT_STATUS" | awk -v prefix="?? $LOG_REL/" 'NF && index($0,prefix) != 1 {print}')"

{
  echo
  echo "utc_end: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "parse_exit_status: $parse_status"
  echo "proof_exit_status: $proof_status"
  echo "positive_witness_exit_status: $attack_status"
  echo "negative_property_exit_status: $unique_status"
  echo "original_regression_exit_status: $original_status"
  echo "impact_wellformedness_status: $impact_wellformedness_status"
  echo "positive_trace_wellformedness_status: $positive_trace_wellformedness_status"
  echo "negative_trace_wellformedness_status: $negative_trace_wellformedness_status"
  echo "original_wellformedness_status: $original_wellformedness_status"
  echo "impact_result_validation_status: $impact_result_validation_status"
  echo "original_result_validation_status: $original_result_validation_status"
  echo "positive_trace_artifact_validation_status: $attack_artifact_validation_status"
  echo "negative_trace_artifact_validation_status: $unique_artifact_validation_status"
  echo "frozen_formula_comparison_status: $formula_comparison_status"
  echo "lower_layer_result_comparison_status: $lower_result_comparison_status"
  echo "post_run_git_status:"
  printf '%s\n' "$POST_RUN_GIT_STATUS"
  echo "post_run_unexpected_status_empty: $([[ -z "$UNEXPECTED_STATUS" ]] && echo true || echo false)"
} >> "$VERSIONS_LOG"

(
  cd "$LOG_DIR"
  find . -maxdepth 1 -type f ! -name 'SHA256SUMS.txt' -printf '%f\n' \
    | LC_ALL=C sort \
    | xargs sha256sum
) > "$MANIFEST_LOG"

cat "$SUMMARY_LOG"

final_status=0
for status in \
  "$parse_status" \
  "$proof_status" \
  "$attack_status" \
  "$unique_status" \
  "$original_status" \
  "$impact_wellformedness_status" \
  "$positive_trace_wellformedness_status" \
  "$negative_trace_wellformedness_status" \
  "$original_wellformedness_status" \
  "$impact_result_validation_status" \
  "$original_result_validation_status" \
  "$attack_artifact_validation_status" \
  "$unique_artifact_validation_status" \
  "$formula_comparison_status" \
  "$lower_result_comparison_status"; do
  if [[ "$status" != "0" ]]; then
    final_status=1
  fi
done
if [[ -n "$UNEXPECTED_STATUS" ]]; then
  echo "error: unexpected post-run worktree changes" >&2
  printf '%s\n' "$UNEXPECTED_STATUS" >&2
  final_status=1
fi

exit "$final_status"
