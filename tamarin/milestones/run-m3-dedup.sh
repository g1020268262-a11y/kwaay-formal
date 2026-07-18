#!/usr/bin/env bash

set -euo pipefail

MODE="fresh"
SOURCE_EVIDENCE=""
MAX_ATTEMPTS=3
PROOF_TIMEOUT_SECONDS=7200

usage() {
  cat >&2 <<'EOF'
usage: run-m3-dedup.sh [--resume-from <evidence-directory> | --verify-only <evidence-directory>]
EOF
}

case "$#" in
  0) ;;
  1)
    [[ "$1" == --self-test ]] || { usage; exit 2; }
    MODE="self-test"
    ;;
  2)
    case "$1" in
      --resume-from) MODE="resume" ;;
      --verify-only) MODE="verify" ;;
      *) usage; exit 2 ;;
    esac
    SOURCE_EVIDENCE="$(readlink -f "$2")"
    ;;
  *) usage; exit 2 ;;
esac

if [[ -n "${KWAAY_REPO_ROOT+x}" ]]; then
  echo "error: KWAAY_REPO_ROOT is not accepted; the runner derives the repository from its own path" >&2
  exit 2
fi

RUNNER_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
RUNNER_DIR="$(dirname "$RUNNER_PATH")"
ROOT_DIR="$(cd "$RUNNER_DIR/../.." && pwd -P)"

RUNNER_REL="tamarin/milestones/run-m3-dedup.sh"
FIXED_REPLAY_REL="tamarin/replay/kwaay_replay_fixed.spthy"
FIXED_IMPACT_REL="tamarin/impact/kwaay_impact_fixed.spthy"
FIXED_REPLAY_README_REL="tamarin/replay/README-fixed.md"
FIXED_IMPACT_README_REL="tamarin/impact/README-fixed.md"
ORIGINAL_REPLAY_REL="tamarin/replay/kwaay_replay_original.spthy"
HMAC_REPLAY_REL="tamarin/replay/kwaay_replay_hmac_only.spthy"
ORIGINAL_IMPACT_REL="tamarin/impact/kwaay_impact_original.spthy"
V6_REL="tamarin/kwaay_splitkem_batch_dynamic_v6.spthy"
V7_REL="tamarin/kwaay_splitkem_batch_dynamic_v7.spthy"
PROVERIF_ORIGINAL_REL="proverif/kwaay_core_final.cpp.pv"
PROVERIF_HMAC_REL="proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv"
PROVERIF_ORIGINAL_BASELINE_REL="logs/final/proverif/summary.txt"
PROVERIF_HMAC_BASELINE_REL="logs/variants/hmac-confirmation/proverif/summary.txt"
LOG_REL="logs/tamarin-m3-dedup"

LOG_DIR="$ROOT_DIR/$LOG_REL"
COMMAND_LOG="$LOG_DIR/command.txt"
VERSIONS_LOG="$LOG_DIR/versions.txt"
SUMMARY_LOG="$LOG_DIR/summary.txt"
FORMULA_LOG="$LOG_DIR/frozen-formula-comparison.txt"
CONSTRUCTOR_LOG="$LOG_DIR/constructor-comparison.txt"
CONSUMER_RULE_LOG="$LOG_DIR/consumer-rule-comparison.txt"
RESULT_VECTOR_LOG="$LOG_DIR/result-vector-comparison.tsv"
MANIFEST_LOG="$LOG_DIR/SHA256SUMS.txt"
ATTEMPT_SUMMARY_LOG="$LOG_DIR/attempt-summary.tsv"
BINDING_LOG="$LOG_DIR/evidence-binding.tsv"
TOOL_BINDING_LOG="$LOG_DIR/tool-binding.tsv"

if [[ "$RUNNER_PATH" != "$ROOT_DIR/$RUNNER_REL" ]]; then
  echo "error: resolved runner path is outside the expected repository location: $RUNNER_PATH" >&2
  exit 2
fi

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

if [[ "$MODE" != "verify" && "$MODE" != "self-test" && -n "$PRE_RUN_GIT_STATUS" ]]; then
  echo "error: pre-run git status is not clean" >&2
  printf '%s\n' "$PRE_RUN_GIT_STATUS" >&2
  exit 2
fi
if [[ "$MODE" != "verify" && "$MODE" != "self-test" && -e "$LOG_DIR" ]]; then
  echo "error: M3 evidence directory already exists: $LOG_DIR" >&2
  exit 2
fi
if [[ ( "$MODE" == "resume" || "$MODE" == "verify" ) && ! -d "$SOURCE_EVIDENCE" ]]; then
  echo "error: evidence directory does not exist: $SOURCE_EVIDENCE" >&2
  exit 2
fi
if [[ "$MODE" == "resume" && "$SOURCE_EVIDENCE" == "$LOG_DIR" ]]; then
  echo "error: resume source and destination must differ" >&2
  exit 2
fi

TRACKED_INPUTS=(
  "$RUNNER_REL"
  "$FIXED_REPLAY_REL"
  "$FIXED_IMPACT_REL"
  "$FIXED_REPLAY_README_REL"
  "$FIXED_IMPACT_README_REL"
  "$ORIGINAL_REPLAY_REL"
  "$HMAC_REPLAY_REL"
  "$ORIGINAL_IMPACT_REL"
  "$V6_REL"
  "$V7_REL"
  "$PROVERIF_ORIGINAL_REL"
  "$PROVERIF_HMAC_REL"
  "$PROVERIF_ORIGINAL_BASELINE_REL"
  "$PROVERIF_HMAC_BASELINE_REL"
)

for path in "${TRACKED_INPUTS[@]}"; do
  if [[ ! -f "$ROOT_DIR/$path" ]]; then
    echo "error: required input missing: $path" >&2
    exit 2
  fi
  if ! "${GIT_CMD[@]}" cat-file -e "$GIT_HEAD:$path" 2>/dev/null; then
    echo "error: required input is not tracked by current HEAD: $path" >&2
    exit 2
  fi
done
if [[ ( "$MODE" == "fresh" || "$MODE" == "resume" ) ]] \
    && ! "${GIT_CMD[@]}" diff --quiet HEAD -- "${TRACKED_INPUTS[@]}"; then
  echo "error: a model, runner, or frozen regression input differs from current HEAD" >&2
  exit 2
fi

declare -A APPROVED_BLOB=()
declare -A APPROVED_SHA256=()
APPROVED_BLOB["$ORIGINAL_REPLAY_REL"]="e3699da2f827a683ded2feaaa7db2d51ad74c023"
APPROVED_SHA256["$ORIGINAL_REPLAY_REL"]="064ec603bdfac917246a12762774701bc624c40ccb11eb6a88adf94befb4322e"
APPROVED_BLOB["$HMAC_REPLAY_REL"]="589e8693f23d76fcf3977d6ca3784a2f670d5d8d"
APPROVED_SHA256["$HMAC_REPLAY_REL"]="d46ead8564b8cc8410f9f3a655c72be440e5fce3f2455022e0b00155508873f6"
APPROVED_BLOB["$ORIGINAL_IMPACT_REL"]="c5cdc0d7233f3a415839b8f289182c0986d911a8"
APPROVED_SHA256["$ORIGINAL_IMPACT_REL"]="0c20e36137c27bd138101a91ef5ce1e16109fccf696f942eb98c3d855a11fa41"

for path in "$ORIGINAL_REPLAY_REL" "$HMAC_REPLAY_REL" "$ORIGINAL_IMPACT_REL"; do
  actual_blob="$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$path")"
  actual_sha="$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
  if [[ "$actual_blob" != "${APPROVED_BLOB[$path]}" ]]; then
    echo "error: frozen blob drift for $path: $actual_blob" >&2
    exit 2
  fi
  if [[ "$actual_sha" != "${APPROVED_SHA256[$path]}" ]]; then
    echo "error: frozen SHA-256 drift for $path: $actual_sha" >&2
    exit 2
  fi
done

BASE_COMMANDS=(sha256sum awk sed grep sort find xargs cmp cp)
PROOF_COMMANDS=(tamarin-prover maude cpp timeout)
for command_name in "${BASE_COMMANDS[@]}"; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "error: required command not found: $command_name" >&2
    exit 2
  fi
done

PROVERIF_CMD=()
PROVERIF_NEEDS_WIN_PATH=0
if [[ "$MODE" == "fresh" || "$MODE" == "resume" ]]; then
  for command_name in "${PROOF_COMMANDS[@]}"; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
      echo "error: required command not found: $command_name" >&2
      exit 2
    fi
  done
fi
if [[ "$MODE" == "verify" || "$MODE" == "self-test" ]]; then
  :
elif command -v proverif >/dev/null 2>&1; then
  PROVERIF_CMD=("$(command -v proverif)")
elif command -v proverif.exe >/dev/null 2>&1; then
  PROVERIF_CMD=("$(command -v proverif.exe)")
  PROVERIF_NEEDS_WIN_PATH=1
elif [[ -x /mnt/d/Proverif/proverif2.05/proverif.exe ]]; then
  PROVERIF_CMD=(/mnt/d/Proverif/proverif2.05/proverif.exe)
  PROVERIF_NEEDS_WIN_PATH=1
else
  echo "error: ProVerif not found" >&2
  exit 2
fi

if [[ "$MODE" == "fresh" || "$MODE" == "resume" ]]; then
  TAMARIN_HELP="$(tamarin-prover --help 2>&1)"
  for option in --output-json --output-dot; do
    if ! grep -q -- "$option" <<<"$TAMARIN_HELP"; then
      echo "error: installed Tamarin does not advertise $option" >&2
      exit 2
    fi
  done
fi

REPLAY_FROZEN=(
  normal_single_accept normal_batch_complete one_send_two_accepts_exists
  same_message_accepted_at_most_once full_message_unique_send
  receiver_accept_has_sender injective_receiver_accept slot_indices_distinct
  process_requires_slot_added process_requires_seal
  complete_requires_all_slots_processed no_add_after_seal no_accept_after_close
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use receiver_state_single_batch
  receiver_state_single_batch_end
)

IMPACT_COMPOSITION=(
  accept_output_has_same_time_accept receiver_accept_has_output
  receiver_accept_has_unique_output accept_id_unique install_has_prior_accept
  install_session_has_interface_origin install_from_accept_has_session
  install_event_has_single_source install_handle_unique
  accept_output_installed_at_most_once distinct_accept_sources_have_distinct_handles
  install_requires_batch_complete consumer_complete_requires_all_outputs_installed
  consumer_complete_single_use no_install_after_consumer_close
  normal_one_accept_one_install normal_consumer_complete
  one_send_two_accepts_two_installs_exists unique_install_within_completed_consumer
)

REPLAY_M3=(
  duplicate_batch_fail_exists duplicate_detected_before_any_accept
  duplicate_batch_has_no_accept process_requires_dedup_pass
  dedup_pass_messages_distinct dedup_decision_single_use
  dedup_outcomes_exclusive normal_distinct_batch_complete
  normal_distinct_fail_slot1_exists normal_distinct_fail_slot2_exists
  batch_fail_complete_exclusive state_consumed_on_duplicate_fail
)

IMPACT_M3=(
  duplicate_batch_fail_exists duplicate_detected_before_any_accept
  duplicate_batch_has_no_accept duplicate_batch_has_no_accept_output
  duplicate_batch_has_no_install process_requires_dedup_pass
  dedup_pass_messages_distinct dedup_decision_single_use
  dedup_outcomes_exclusive normal_distinct_batch_complete
  normal_distinct_consumer_complete normal_distinct_fail_slot1_exists
  normal_distinct_fail_slot2_exists batch_fail_complete_exclusive
  state_consumed_on_duplicate_fail no_consumer_after_failed_batch
)

HMAC_REPLAY_LEMMAS=(
  normal_confirmed_single_accept normal_confirmed_batch_complete
  confirmed_receiver_accept_has_sender confirmed_message_unique_send
  one_confirmed_send_two_accepts_exists confirmed_message_accepted_at_most_once
  injective_confirmed_receiver_accept slot_indices_distinct
  process_requires_slot_added process_requires_seal
  complete_requires_all_slots_processed no_add_after_seal no_accept_after_close
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use receiver_state_single_batch
  receiver_state_single_batch_end
)

V6_LEMMAS=(
  executable_add_slot executable_seal_batch executable_process_slot
  executable_batch_complete executable_batch_fail process_requires_slot_added
  process_requires_seal complete_requires_seal fail_requires_seal
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use batch_fail_complete_exclusive
  slot_origin_without_early_compromise slot_key_known_requires_exception
  partnered_slot_key_not_attacker_known_without_early_compromise
)

V7_LEMMAS=(
  executable_four_slots_added executable_seal_batch executable_four_slots_processed
  executable_batch_complete executable_batch_fail seal_requires_all_slots_added
  process_requires_slot_added process_requires_seal complete_requires_seal
  fail_requires_seal complete_requires_all_slots_done
  complete_requires_all_added_slots_processed no_add_after_seal
  no_add_after_complete no_add_after_fail no_slot_accept_after_complete
  no_slot_accept_after_fail no_slot_accept_after_close
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use batch_fail_complete_exclusive
  receiver_state_single_batch_end slot_origin
)

FIXED_REPLAY_LEMMAS=("${REPLAY_FROZEN[@]}" "${REPLAY_M3[@]}")
FIXED_IMPACT_LEMMAS=("${IMPACT_COMPOSITION[@]}" "${REPLAY_FROZEN[@]}" "${IMPACT_M3[@]}")
ORIGINAL_IMPACT_LEMMAS=("${IMPACT_COMPOSITION[@]}" "${REPLAY_FROZEN[@]}")

declare -A FIXED_REPLAY_EXPECTED=()
declare -A FIXED_IMPACT_EXPECTED=()
declare -A ORIGINAL_REPLAY_EXPECTED=()
declare -A HMAC_REPLAY_EXPECTED=()
declare -A ORIGINAL_IMPACT_EXPECTED=()
declare -A V6_EXPECTED=()
declare -A V7_EXPECTED=()

for lemma in "${FIXED_REPLAY_LEMMAS[@]}"; do FIXED_REPLAY_EXPECTED["$lemma"]="verified"; done
FIXED_REPLAY_EXPECTED[one_send_two_accepts_exists]="falsified"

for lemma in "${FIXED_IMPACT_LEMMAS[@]}"; do FIXED_IMPACT_EXPECTED["$lemma"]="verified"; done
FIXED_IMPACT_EXPECTED[one_send_two_accepts_exists]="falsified"
FIXED_IMPACT_EXPECTED[normal_consumer_complete]="falsified"
FIXED_IMPACT_EXPECTED[one_send_two_accepts_two_installs_exists]="falsified"

for lemma in "${REPLAY_FROZEN[@]}"; do ORIGINAL_REPLAY_EXPECTED["$lemma"]="verified"; done
ORIGINAL_REPLAY_EXPECTED[same_message_accepted_at_most_once]="falsified"
ORIGINAL_REPLAY_EXPECTED[injective_receiver_accept]="falsified"

for lemma in "${HMAC_REPLAY_LEMMAS[@]}"; do HMAC_REPLAY_EXPECTED["$lemma"]="verified"; done
HMAC_REPLAY_EXPECTED[confirmed_message_accepted_at_most_once]="falsified"
HMAC_REPLAY_EXPECTED[injective_confirmed_receiver_accept]="falsified"

for lemma in "${ORIGINAL_IMPACT_LEMMAS[@]}"; do ORIGINAL_IMPACT_EXPECTED["$lemma"]="verified"; done
ORIGINAL_IMPACT_EXPECTED[unique_install_within_completed_consumer]="falsified"
ORIGINAL_IMPACT_EXPECTED[same_message_accepted_at_most_once]="falsified"
ORIGINAL_IMPACT_EXPECTED[injective_receiver_accept]="falsified"

for lemma in "${V6_LEMMAS[@]}"; do V6_EXPECTED["$lemma"]="verified"; done
for lemma in "${V7_LEMMAS[@]}"; do V7_EXPECTED["$lemma"]="verified"; done

detect_eol() {
  local file="$1"
  if LC_ALL=C grep -q $'\r$' "$file"; then
    if LC_ALL=C grep -qv $'\r$' "$file"; then printf 'mixed-or-CRLF\n'; else printf 'CRLF\n'; fi
  else
    printf 'LF\n'
  fi
}

print_command() {
  local label="$1"; shift
  printf '%s:' "$label"
  printf ' %q' "$@"
  printf '\n'
}

extract_result_rows() {
  local source="$1"
  awk '
    /^summary of summaries:[[:space:]]*$/ { in_summary=1; next }
    in_summary && /^  [[:alnum:]_]+ \((all-traces|exists-trace)\): / {
      line=$0; sub(/\r$/, "", line)
      name=line; sub(/^  /, "", name); sub(/ .*/, "", name)
      detail=line; sub(/^.*: /, "", detail)
      status="nonterminal"; steps="-"
      if (line ~ /: verified \([0-9]+ steps\)$/) {
        status="verified"; steps=line; sub(/^.*\(/, "", steps); sub(/ steps\)$/, "", steps)
      } else if (line ~ /: falsified - (found trace|no trace found) \([0-9]+ steps\)$/) {
        status="falsified"; steps=line; sub(/^.*\(/, "", steps); sub(/ steps\)$/, "", steps)
      }
      gsub(/\t/, " ", detail)
      print name "\t" status "\t" steps "\t" detail
    }
  ' "$source"
}

check_wellformedness_success() {
  local file="$1"
  [[ -s "$file" ]] || return 1
  awk '{ sub(/\r$/, "") } $0 == "/* All wellformedness checks were successful. */" { found=1 } END { exit(found ? 0 : 1) }' "$file" || return 1
  ! grep -Eiq 'WARNING:.*wellformedness|wellformedness.*(warning|errors?|failed)|Wellformedness-error|partial deconstructions? left' "$file"
}

classify_attempt() {
  local lemma="$1" exit_status="$2" raw_file="$3" destination="$4"
  local rows="$TMP_DIR/classify-${RANDOM}-${RANDOM}.tsv" status="missing" steps="-" detail="MISSING"
  local wellformedness="failure" loop_marker="false" timeout_marker="false"
  local terminal="false" retry_eligible="false" target_count=0 other_terminal_count=0
  : > "$rows"
  if [[ -s "$raw_file" ]]; then
    extract_result_rows "$raw_file" > "$rows"
    target_count="$(awk -F '\t' -v target="$lemma" '$1 == target {n++} END {print n+0}' "$rows")"
    other_terminal_count="$(awk -F '\t' -v target="$lemma" '$1 != target && ($2 == "verified" || $2 == "falsified") {n++} END {print n+0}' "$rows")"
    if [[ "$target_count" -eq 1 ]]; then
      IFS=$'\t' read -r _ status steps detail < <(awk -F '\t' -v target="$lemma" '$1 == target {print; exit}' "$rows")
    else
      status="missing"; detail="target-summary-count=$target_count"
    fi
    if check_wellformedness_success "$raw_file"; then wellformedness="success"; fi
    if grep -Fq '<<loop>>' "$raw_file"; then loop_marker="true"; fi
    if grep -Eiq '(^|[^[:alpha:]])time(d)?[ -]?out([^[:alpha:]]|$)|timeout:|timed out' "$raw_file"; then timeout_marker="true"; fi
  fi
  [[ "$exit_status" == 124 ]] && timeout_marker="true"
  if [[ "$exit_status" == 0 && "$wellformedness" == success && "$loop_marker" == false \
        && "$timeout_marker" == false && "$target_count" -eq 1 && "$other_terminal_count" -eq 0 \
        && ( "$status" == verified || "$status" == falsified ) ]]; then
    terminal="true"
  elif [[ "$exit_status" != 0 || "$status" == missing || "$status" == nonterminal \
          || "$loop_marker" == true || "$timeout_marker" == true ]]; then
    retry_eligible="true"
  fi
  detail="${detail//$'\t'/ }"
  {
    printf 'status\tsteps\texit_status\twellformedness\tloop_marker\ttimeout_marker\tterminal\tretry_eligible\traw_result\n'
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$status" "$steps" "$exit_status" "$wellformedness" "$loop_marker" "$timeout_marker" \
      "$terminal" "$retry_eligible" "$detail"
  } > "$destination"
  rm -f "$rows"
}

attempt_field() {
  local meta="$1" column="$2"
  awk -F '\t' -v wanted="$column" '
    NR == 1 { for (i=1; i<=NF; i++) if ($i == wanted) field=i; next }
    NR == 2 && field { print $field }
  ' "$meta"
}

invoke_proof_attempt() {
  local suite="$1" lemma="$2" model_rel="$3" attempt="$4" target_dir="$5"
  local raw="$target_dir/attempt-$attempt.out" exit_file="$target_dir/attempt-$attempt.exit"
  local origin_file="$target_dir/attempt-$attempt.origin" status
  [[ ! -e "$raw" && ! -e "$exit_file" && ! -e "$origin_file" ]] || {
    echo "error: refusing to overwrite attempt $attempt for $suite/$lemma" >&2
    return 2
  }
  {
    print_command "executed-proof[$suite][$lemma][attempt-$attempt]" timeout --foreground "$PROOF_TIMEOUT_SECONDS" \
      tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$model_rel"
    echo "raw_output[$suite][$lemma][attempt-$attempt]: ${raw#"$ROOT_DIR/"}"
  } >> "$COMMAND_LOG"
  set +e
  timeout --foreground "$PROOF_TIMEOUT_SECONDS" tamarin-prover --derivcheck-timeout=0 \
    "--prove=$lemma" "$model_rel" > "$raw" 2>&1
  status=$?
  set -e
  printf '%s\n' "$status" > "$exit_file"
  printf 'executed-by-current-runner\n' > "$origin_file"
}

evaluate_target_attempts() {
  local suite="$1" lemma="$2" model_rel="$3" aggregate="$4" allow_run="$5" verify_metadata="$6"
  local target_dir="$LOG_DIR/proofs/$suite/$lemma" meta_tmp raw exit_file origin_file exit_status
  local -a attempts=() terminal_statuses=() terminal_attempts=()
  local attempt expected_attempt=1 status steps wf loop timeout_marker terminal eligible detail origin reused
  local selected="" selected_meta="" attempt_count=0 errors=0 last_eligible="false"
  if [[ "$verify_metadata" == true ]]; then
    [[ -d "$target_dir" ]] || { echo "error: proof target directory missing for $suite/$lemma" >&2; return 1; }
  else
    mkdir -p "$target_dir"
  fi

  shopt -s nullglob
  attempts=("$target_dir"/attempt-*.out)
  shopt -u nullglob
  if [[ "${#attempts[@]}" -gt 0 ]]; then
    mapfile -t attempts < <(printf '%s\n' "${attempts[@]}" | LC_ALL=C sort -V)
  fi
  for raw in "${attempts[@]}"; do
    attempt="${raw##*/attempt-}"; attempt="${attempt%.out}"
    if [[ "$attempt" != "$expected_attempt" || "$attempt" -gt "$MAX_ATTEMPTS" ]]; then
      echo "error: non-contiguous or excessive attempts for $suite/$lemma" >&2
      errors=1
    fi
    expected_attempt=$((expected_attempt + 1)); attempt_count=$((attempt_count + 1))
    exit_file="$target_dir/attempt-$attempt.exit"
    origin_file="$target_dir/attempt-$attempt.origin"
    [[ -s "$exit_file" && -s "$origin_file" ]] || { echo "error: incomplete attempt metadata for $suite/$lemma/$attempt" >&2; errors=1; continue; }
    exit_status="$(tr -d '\r\n' < "$exit_file")"
    [[ "$exit_status" =~ ^[0-9]+$ ]] || { echo "error: invalid exit status for $suite/$lemma/$attempt" >&2; errors=1; continue; }
    meta_tmp="$TMP_DIR/meta-$suite-$lemma-$attempt.tsv"
    classify_attempt "$lemma" "$exit_status" "$raw" "$meta_tmp"
    if [[ "$verify_metadata" == true ]]; then
      cmp -s "$meta_tmp" "$target_dir/attempt-$attempt.meta.tsv" || { echo "error: attempt metadata mismatch for $suite/$lemma/$attempt" >&2; errors=1; }
    else
      cp "$meta_tmp" "$target_dir/attempt-$attempt.meta.tsv"
    fi
    status="$(attempt_field "$meta_tmp" status)"; steps="$(attempt_field "$meta_tmp" steps)"
    wf="$(attempt_field "$meta_tmp" wellformedness)"; loop="$(attempt_field "$meta_tmp" loop_marker)"
    timeout_marker="$(attempt_field "$meta_tmp" timeout_marker)"; terminal="$(attempt_field "$meta_tmp" terminal)"
    eligible="$(attempt_field "$meta_tmp" retry_eligible)"; detail="$(attempt_field "$meta_tmp" raw_result)"
    origin="$(tr -d '\r\n' < "$origin_file")"
    [[ "$origin" == imported || "$origin" == executed-by-current-runner ]] || { echo "error: invalid attempt origin for $suite/$lemma/$attempt" >&2; errors=1; }
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$suite" "$lemma" "$attempt" "$exit_status" "$status" "$wf" "$loop" "$timeout_marker" \
      "$terminal" "$eligible" "$origin" "proofs/$suite/$lemma/attempt-$attempt.out" >> "$ATTEMPT_SUMMARY_LOG"
    last_eligible="$eligible"
    if [[ "$terminal" == true ]]; then
      terminal_statuses+=("$status"); terminal_attempts+=("$attempt")
    fi
  done

  if [[ "${#terminal_statuses[@]}" -gt 1 ]]; then
    for status in "${terminal_statuses[@]}"; do
      [[ "$status" == "${terminal_statuses[0]}" ]] || { echo "error: inconsistent terminal attempts for $suite/$lemma" >&2; errors=1; }
    done
  fi

  while [[ "${#terminal_statuses[@]}" -eq 0 && "$allow_run" == true && "$errors" -eq 0 \
           && "$attempt_count" -lt "$MAX_ATTEMPTS" ]]; do
    if [[ "$attempt_count" -gt 0 && "$last_eligible" != true ]]; then
      echo "error: nonterminal attempt is not retry-eligible for $suite/$lemma" >&2
      errors=1; break
    fi
    attempt=$((attempt_count + 1))
    invoke_proof_attempt "$suite" "$lemma" "$model_rel" "$attempt" "$target_dir" || { errors=1; break; }
    raw="$target_dir/attempt-$attempt.out"; exit_file="$target_dir/attempt-$attempt.exit"
    exit_status="$(tr -d '\r\n' < "$exit_file")"; meta_tmp="$TMP_DIR/meta-$suite-$lemma-$attempt.tsv"
    classify_attempt "$lemma" "$exit_status" "$raw" "$meta_tmp"
    cp "$meta_tmp" "$target_dir/attempt-$attempt.meta.tsv"
    status="$(attempt_field "$meta_tmp" status)"; steps="$(attempt_field "$meta_tmp" steps)"
    wf="$(attempt_field "$meta_tmp" wellformedness)"; loop="$(attempt_field "$meta_tmp" loop_marker)"
    timeout_marker="$(attempt_field "$meta_tmp" timeout_marker)"; terminal="$(attempt_field "$meta_tmp" terminal)"
    eligible="$(attempt_field "$meta_tmp" retry_eligible)"; detail="$(attempt_field "$meta_tmp" raw_result)"
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$suite" "$lemma" "$attempt" "$exit_status" "$status" "$wf" "$loop" "$timeout_marker" \
      "$terminal" "$eligible" executed-by-current-runner "proofs/$suite/$lemma/attempt-$attempt.out" >> "$ATTEMPT_SUMMARY_LOG"
    attempt_count=$attempt; last_eligible="$eligible"
    if [[ "$terminal" == true ]]; then terminal_statuses+=("$status"); terminal_attempts+=("$attempt"); fi
  done

  if [[ "${#terminal_attempts[@]}" -gt 0 ]]; then
    selected="${terminal_attempts[0]}"
    selected_meta="$target_dir/attempt-$selected.meta.tsv"
    if [[ "$verify_metadata" == true ]]; then
      [[ -s "$target_dir/selected-attempt.txt" ]] && [[ "$(tr -d '\r\n' < "$target_dir/selected-attempt.txt")" == "$selected" ]] \
        || { echo "error: selected attempt mismatch for $suite/$lemma" >&2; errors=1; }
    else
      printf '%s\n' "$selected" > "$target_dir/selected-attempt.txt"
    fi
    status="$(attempt_field "$selected_meta" status)"; steps="$(attempt_field "$selected_meta" steps)"
    exit_status="$(attempt_field "$selected_meta" exit_status)"; wf="$(attempt_field "$selected_meta" wellformedness)"
    loop="$(attempt_field "$selected_meta" loop_marker)"; timeout_marker="$(attempt_field "$selected_meta" timeout_marker)"
    detail="$(attempt_field "$selected_meta" raw_result)"
    origin="$(tr -d '\r\n' < "$target_dir/attempt-$selected.origin")"
    [[ "$origin" == imported ]] && reused=true || reused=false
  else
    selected="-"; reused=false; errors=1
    if [[ "$attempt_count" -gt 0 ]]; then
      selected_meta="$target_dir/attempt-$attempt_count.meta.tsv"
      status="$(attempt_field "$selected_meta" status)"; steps="$(attempt_field "$selected_meta" steps)"
      exit_status="$(attempt_field "$selected_meta" exit_status)"; wf="$(attempt_field "$selected_meta" wellformedness)"
      loop="$(attempt_field "$selected_meta" loop_marker)"; timeout_marker="$(attempt_field "$selected_meta" timeout_marker)"
      detail="$(attempt_field "$selected_meta" raw_result)"
    else
      status=missing; steps=-; exit_status=-; wf=failure; loop=false; timeout_marker=false; detail=NO_ATTEMPTS
    fi
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$lemma" "$status" "$steps" "$exit_status" "$wf" "$loop" "$timeout_marker" "$attempt_count" \
    "$selected" "$reused" "proofs/$suite/$lemma" "$detail" >> "$aggregate"
  return "$errors"
}

validate_suite() {
  local suite="$1" aggregate="$2" names_var="$3" expected_var="$4"
  local -n names_ref="$names_var" expected_ref="$expected_var"
  local rows="$TMP_DIR/${suite}-aggregate.tsv" errors=0 index=0 lemma actual expected
  tail -n +2 "$aggregate" > "$rows"
  printf 'suite\tlemma\tactual_status\texpected_status\tmatch\n' > "$TMP_DIR/${suite}-vector.tsv"
  while IFS=$'\t' read -r lemma actual _; do
    expected="${expected_ref[$lemma]-MISSING}"
    if [[ "$actual" == "$expected" ]]; then match=MATCH; else match=MISMATCH; errors=1; fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$suite" "$lemma" "$actual" "$expected" "$match" >> "$TMP_DIR/${suite}-vector.tsv"
    if [[ "${names_ref[$index]-MISSING}" != "$lemma" ]]; then errors=1; fi
    index=$((index + 1))
  done < "$rows"
  [[ "$index" -eq "${#names_ref[@]}" ]] || errors=1
  tail -n +2 "$TMP_DIR/${suite}-vector.tsv" >> "$RESULT_VECTOR_LOG"
  return "$errors"
}

run_tamarin_suite() {
  local suite="$1" model_rel="$2" names_var="$3" expected_var="$4"
  local -n names_ref="$names_var"
  local proof_dir="$LOG_DIR/proofs/$suite" aggregate="$LOG_DIR/aggregate-$suite.tsv"
  local lemma suite_errors=0
  mkdir -p "$proof_dir"
  printf 'lemma\tstatus\tsteps\texit_status\twellformedness\tloop_marker\ttimeout_marker\tattempt_count\tselected_attempt\treused\tsource_directory\traw_result\n' > "$aggregate"
  for lemma in "${names_ref[@]}"; do
    if ! evaluate_target_attempts "$suite" "$lemma" "$model_rel" "$aggregate" true false; then suite_errors=1; fi
  done
  if ! validate_suite "$suite" "$aggregate" "$names_var" "$expected_var"; then suite_errors=1; fi
  return "$suite_errors"
}

extract_lemma_formula_block() {
  local source="$1" lemma="$2" destination="$3"
  awk -v target="$lemma" '
    { sub(/\r$/, "") }
    $0 == "lemma " target ":" { found=1 }
    found {
      print
      if ($0 ~ /^[[:space:]]*"/) in_formula=1
      if (in_formula && $0 ~ /"[[:space:]]*$/) { closed=1; exit }
    }
    END { if (!found || !closed) exit 1 }
  ' "$source" > "$destination"
}

compare_formula_set() {
  local label="$1" source="$2" target="$3" names_var="$4"
  local -n names_ref="$names_var"
  local lemma a b ah bh match errors=0
  for lemma in "${names_ref[@]}"; do
    a="$TMP_DIR/${label}-source-$lemma"; b="$TMP_DIR/${label}-target-$lemma"
    if extract_lemma_formula_block "$source" "$lemma" "$a" && extract_lemma_formula_block "$target" "$lemma" "$b"; then
      ah="$(sha256sum "$a" | awk '{print $1}')"; bh="$(sha256sum "$b" | awk '{print $1}')"
      if cmp -s "$a" "$b"; then match=MATCH; else match=MISMATCH; errors=1; fi
    else
      ah=EXTRACTION_ERROR; bh=EXTRACTION_ERROR; match=MISMATCH; errors=1
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$lemma" "$ah" "$bh" "$match" >> "$FORMULA_LOG"
  done
  return "$errors"
}

extract_functions_block() {
  local source="$1" destination="$2"
  awk '
    { sub(/\r$/, "") }
    $0 == "functions:" { found=1 }
    found && NF == 0 { exit }
    found { print }
    END { if (!found) exit 1 }
  ' "$source" > "$destination"
}

compare_constructors() {
  local label="$1"
  local source="$2"
  local target="$3"
  local a="$TMP_DIR/${label}-functions-a"
  local b="$TMP_DIR/${label}-functions-b"
  local match

  extract_functions_block "$source" "$a"
  extract_functions_block "$target" "$b"

  if cmp -s "$a" "$b"; then
    match=MATCH
  else
    match=MISMATCH
  fi

  printf '%s\t%s\t%s\t%s\n' \
    "$label" \
    "$(sha256sum "$a" | awk '{print $1}')" \
    "$(sha256sum "$b" | awk '{print $1}')" \
    "$match" >> "$CONSTRUCTOR_LOG"

  [[ "$match" == MATCH ]]
}

extract_rule_block() {
  local source="$1" rule="$2" destination="$3"
  awk -v target="$rule" '
    { sub(/\r$/, "") }
    $0 == "rule " target ":" { found=1 }
    found && NF == 0 { exit }
    found { print }
    END { if (!found) exit 1 }
  ' "$source" > "$destination"
}

compare_consumer_rules() {
  local rule a b match errors=0
  printf 'rule\toriginal_sha256\tfixed_sha256\tmatch\n' > "$CONSUMER_RULE_LOG"
  for rule in InstallAcceptedOutputFirst InstallAcceptedOutputSecond CompleteConsumer; do
    a="$TMP_DIR/consumer-a-$rule"; b="$TMP_DIR/consumer-b-$rule"
    extract_rule_block "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$rule" "$a"
    extract_rule_block "$ROOT_DIR/$FIXED_IMPACT_REL" "$rule" "$b"
    if cmp -s "$a" "$b"; then match=MATCH; else match=MISMATCH; errors=1; fi
    printf '%s\t%s\t%s\t%s\n' "$rule" "$(sha256sum "$a" | awk '{print $1}')" "$(sha256sum "$b" | awk '{print $1}')" "$match" >> "$CONSUMER_RULE_LOG"
  done
  return "$errors"
}

extract_baseline_target_results() {
  local summary="$1" target="$2" destination="$3"
  awk -v target="$target" '
    $0 == "TARGET: " target { in_target=1; next }
    in_target && /^TARGET: / { exit }
    in_target && /^RESULT / { sub(/\r$/, ""); print }
  ' "$summary" | LC_ALL=C sort > "$destination"
  [[ -s "$destination" ]]
}

run_proverif_target() {
  local suite="$1"
  local target="$2"
  local model_rel="$3"
  local baseline_rel="$4"
  local dir="$LOG_DIR/regressions/$suite"
  local generated="$dir/generated/$target.pv"
  local raw="$dir/$target.out"
  local cpp_err="$dir/$target.cpp.err"
  local input status errors=0
  local actual="$TMP_DIR/$suite-$target-actual"
  local baseline="$TMP_DIR/$suite-$target-baseline"
  local match
  mkdir -p "$dir/generated"
  print_command "executed-proverif-cpp[$suite][$target]" cpp -P -D "$target" "$ROOT_DIR/$model_rel" >> "$COMMAND_LOG"
  set +e
  cpp -P -D "$target" "$ROOT_DIR/$model_rel" > "$generated" 2> "$cpp_err"
  status=$?
  set -e
  if [[ "$status" -ne 0 ]]; then errors=1; : > "$raw"; else
    input="$generated"
    if [[ "$PROVERIF_NEEDS_WIN_PATH" -eq 1 ]] && command -v wslpath >/dev/null 2>&1; then input="$(wslpath -w "$generated")"; fi
    {
      print_command "executed-proverif[$suite][$target]" timeout 300 "${PROVERIF_CMD[@]}" "$input"
      echo "raw_output[$suite][$target]: ${raw#"$ROOT_DIR/"}"
    } >> "$COMMAND_LOG"
    set +e
    timeout 300 "${PROVERIF_CMD[@]}" "$input" > "$raw" 2>&1
    status=$?
    set -e
    [[ "$status" -eq 0 ]] || errors=1
  fi
  grep '^RESULT' "$raw" | sed 's/\r$//' | LC_ALL=C sort > "$actual" || true
  if ! extract_baseline_target_results "$ROOT_DIR/$baseline_rel" "$target" "$baseline"; then errors=1; fi
  if [[ -s "$actual" ]] && cmp -s "$actual" "$baseline"; then match=MATCH; else match=MISMATCH; errors=1; fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$status" "$match" "regressions/$suite/$target.out" >> "$LOG_DIR/proverif-result-comparison.tsv"
  return "$errors"
}

run_trace() {
  local label="$1"
  local model_rel="$2"
  local lemma="$3"
  local dir="$LOG_DIR/traces/$label"
  local raw="$dir/trace.out"
  local json="$dir/trace.json"
  local dot="$dir/trace.dot"
  local status errors=0
  mkdir -p "$dir"
  {
    print_command "executed-trace[$label]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" --output-json="$json" --output-dot="$dot" "$model_rel"
    echo "raw_output[trace][$label]: ${raw#"$ROOT_DIR/"}"
  } >> "$COMMAND_LOG"
  set +e
  tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" --output-json="$json" --output-dot="$dot" "$model_rel" > "$raw" 2>&1
  status=$?
  set -e
  [[ "$status" -eq 0 && -s "$raw" && -s "$json" && -s "$dot" ]] || errors=1
  check_wellformedness_success "$raw" || errors=1
  grep -Eq "^  ${lemma} \(exists-trace\): verified \([0-9]+ steps\)\r?$" "$raw" || errors=1
  grep -Fq '<<loop>>' "$raw" && errors=1
  return "$errors"
}

manifest_is_valid() {
  local evidence="$1" output="$2"
  [[ -s "$evidence/SHA256SUMS.txt" ]] || return 1
  (cd "$evidence" && sha256sum -c SHA256SUMS.txt) > "$output" 2>&1
}

version_metadata_value() {
  local versions="$1" path="$2" field="$3"
  awk -v target="$path" -v wanted="$field" '
    $0 == "path: " target { in_path=1; next }
    in_path && /^path: / { exit }
    in_path && $0 ~ "^  " wanted ": " { sub("^  " wanted ": ", ""); print; exit }
  ' "$versions"
}

validate_legacy_binding() {
  local evidence="$1" versions="$evidence/versions.txt" source_head source_tree actual_tree
  local path recorded_blob recorded_sha object_file object_sha current_blob current_sha
  [[ -s "$versions" ]] || { echo "error: imported versions.txt missing" >&2; return 1; }
  source_head="$(awk -F ': ' '$1 == "git_head" {print $2; exit}' "$versions")"
  source_tree="$(awk -F ': ' '$1 == "git_tree" {print $2; exit}' "$versions")"
  [[ "$source_head" =~ ^[0-9a-f]{40}$ && "$source_tree" =~ ^[0-9a-f]{40}$ ]] || {
    echo "error: imported execution HEAD/tree missing" >&2; return 1;
  }
  "${GIT_CMD[@]}" cat-file -e "$source_head^{commit}" 2>/dev/null || { echo "error: imported HEAD object unavailable" >&2; return 1; }
  actual_tree="$("${GIT_CMD[@]}" show -s --format=%T "$source_head")"
  [[ "$actual_tree" == "$source_tree" ]] || { echo "error: imported execution tree mismatch" >&2; return 1; }
  for path in "${TRACKED_INPUTS[@]}"; do
    recorded_blob="$(version_metadata_value "$versions" "$path" blob_oid)"
    recorded_sha="$(version_metadata_value "$versions" "$path" sha256)"
    [[ "$recorded_blob" =~ ^[0-9a-f]{40}$ && "$recorded_sha" =~ ^[0-9a-f]{64}$ ]] || {
      echo "error: imported input metadata missing for $path" >&2; return 1;
    }
    [[ "$("${GIT_CMD[@]}" rev-parse "$source_head:$path")" == "$recorded_blob" ]] || {
      echo "error: imported blob binding mismatch for $path" >&2; return 1;
    }
    object_file="$TMP_DIR/source-object-${RANDOM}"
    "${GIT_CMD[@]}" cat-file blob "$source_head:$path" > "$object_file"
    object_sha="$(sha256sum "$object_file" | awk '{print $1}')"
    [[ "$object_sha" == "$recorded_sha" ]] || { echo "error: imported SHA-256 binding mismatch for $path" >&2; return 1; }
    if [[ "$path" != "$RUNNER_REL" ]]; then
      current_blob="$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$path")"
      current_sha="$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
      [[ "$current_blob" == "$recorded_blob" && "$current_sha" == "$recorded_sha" ]] || {
        echo "error: proof input differs between imported run and current runner: $path" >&2; return 1;
      }
    fi
  done

  local source_tamarin source_maude source_proverif live_versions live_tamarin live_maude live_proverif pv_status
  source_tamarin="$(grep -m1 '^Tamarin version ' "$versions" | sed 's/^Tamarin version //')"
  source_maude="$(grep -m1 '^Maude version ' "$versions" | sed 's/^Maude version //')"
  source_proverif="$(grep -m1 '^Proverif [0-9]' "$versions" | awk '{print $2}' | tr -d '.')"
  live_versions="$TMP_DIR/live-tool-versions.txt"
  tamarin-prover --version > "$live_versions" 2>&1
  live_tamarin="$(grep -m1 '^Tamarin version ' "$live_versions" | sed 's/^Tamarin version //')"
  live_maude="$(maude --version 2>&1 | sed -n '1{s/\r$//;p;}')"
  set +e
  "${PROVERIF_CMD[@]}" -version > "$TMP_DIR/live-proverif-version.txt" 2>&1
  pv_status=$?
  set -e
  live_proverif="$(grep -m1 '^Proverif [0-9]' "$TMP_DIR/live-proverif-version.txt" | awk '{print $2}' | tr -d '.')"
  [[ -n "$source_tamarin" && "$source_tamarin" == "$live_tamarin" ]] || { echo "error: imported Tamarin version mismatch" >&2; return 1; }
  [[ -n "$source_maude" && "$source_maude" == "$live_maude" ]] || { echo "error: imported Maude version mismatch" >&2; return 1; }
  [[ -n "$source_proverif" && "$source_proverif" == "$live_proverif" ]] || { echo "error: imported ProVerif version mismatch" >&2; return 1; }
  : "$pv_status"
}

validate_imported_comparisons() {
  local evidence="$1" saved_formula="$FORMULA_LOG" saved_constructor="$CONSTRUCTOR_LOG" saved_consumer="$CONSUMER_RULE_LOG"
  local errors=0
  FORMULA_LOG="$TMP_DIR/import-formulas.tsv"
  CONSTRUCTOR_LOG="$TMP_DIR/import-constructors.tsv"
  CONSUMER_RULE_LOG="$TMP_DIR/import-consumers.tsv"
  printf 'scope\tlemma\tsource_sha256\tfixed_sha256\tmatch\n' > "$FORMULA_LOG"
  compare_formula_set replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" "$ROOT_DIR/$FIXED_REPLAY_REL" REPLAY_FROZEN || errors=1
  compare_formula_set impact-composition "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" IMPACT_COMPOSITION || errors=1
  compare_formula_set impact-lower "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" REPLAY_FROZEN || errors=1
  printf 'scope\tsource_sha256\tfixed_sha256\tmatch\n' > "$CONSTRUCTOR_LOG"
  compare_constructors replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" "$ROOT_DIR/$FIXED_REPLAY_REL" || errors=1
  compare_constructors impact "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" || errors=1
  compare_consumer_rules || errors=1
  cmp -s "$FORMULA_LOG" "$evidence/frozen-formula-comparison.txt" || errors=1
  cmp -s "$CONSTRUCTOR_LOG" "$evidence/constructor-comparison.txt" || errors=1
  cmp -s "$CONSUMER_RULE_LOG" "$evidence/consumer-rule-comparison.txt" || errors=1
  FORMULA_LOG="$saved_formula"; CONSTRUCTOR_LOG="$saved_constructor"; CONSUMER_RULE_LOG="$saved_consumer"
  [[ "$errors" -eq 0 ]] || { echo "error: imported formula/constructor/consumer comparison failed" >&2; return 1; }
}

validate_imported_proverif() {
  local evidence="$1" suite target baseline_rel raw actual baseline row errors=0
  local -a cases=(
    'proverif-original|BASELINE|logs/final/proverif/summary.txt'
    'proverif-original|COMPONENT|logs/final/proverif/summary.txt'
    'proverif-hmac|HMAC_BASELINE|logs/variants/hmac-confirmation/proverif/summary.txt'
    'proverif-hmac|HMAC_COMPONENT|logs/variants/hmac-confirmation/proverif/summary.txt'
  )
  [[ "$(awk 'END {print NR+0}' "$evidence/proverif-result-comparison.tsv")" -eq 5 ]] || errors=1
  for row in "${cases[@]}"; do
    IFS='|' read -r suite target baseline_rel <<< "$row"
    raw="$evidence/regressions/$suite/$target.out"
    [[ -s "$raw" ]] || { errors=1; continue; }
    [[ "$(awk -F '\t' -v s="$suite" -v t="$target" '$1==s && $2==t && $3==0 && $4=="MATCH" {n++} END{print n+0}' "$evidence/proverif-result-comparison.tsv")" -eq 1 ]] || errors=1
    actual="$TMP_DIR/pv-$suite-$target-actual"; baseline="$TMP_DIR/pv-$suite-$target-baseline"
    grep '^RESULT' "$raw" | sed 's/\r$//' | LC_ALL=C sort > "$actual" || true
    extract_baseline_target_results "$ROOT_DIR/$baseline_rel" "$target" "$baseline" || errors=1
    [[ -s "$actual" ]] && cmp -s "$actual" "$baseline" || errors=1
  done
  [[ "$errors" -eq 0 ]] || { echo "error: imported ProVerif regression validation failed" >&2; return 1; }
}

validate_imported_traces() {
  local evidence="$1" row label lemma dir errors=0
  local -a cases=(
    'duplicate-fail|duplicate_batch_fail_exists'
    'distinct-complete|normal_distinct_batch_complete'
    'distinct-fail-slot1|normal_distinct_fail_slot1_exists'
    'distinct-fail-slot2|normal_distinct_fail_slot2_exists'
    'distinct-consumer|normal_distinct_consumer_complete'
  )
  for row in "${cases[@]}"; do
    IFS='|' read -r label lemma <<< "$row"; dir="$evidence/traces/$label"
    [[ -s "$dir/trace.out" && -s "$dir/trace.json" && -s "$dir/trace.dot" ]] || { errors=1; continue; }
    check_wellformedness_success "$dir/trace.out" || errors=1
    grep -Eq "^  ${lemma} \(exists-trace\): verified \([0-9]+ steps\)\r?$" "$dir/trace.out" || errors=1
    ! grep -Fq '<<loop>>' "$dir/trace.out" || errors=1
  done
  [[ "$errors" -eq 0 ]] || { echo "error: imported trace validation failed" >&2; return 1; }
}

legacy_aggregate_value() {
  local aggregate="$1" lemma="$2" field="$3"
  awk -F '\t' -v target="$lemma" -v wanted="$field" '
    NR==1 { for(i=1;i<=NF;i++) if($i==wanted) column=i; next }
    $1==target && column { print $column }
  ' "$aggregate"
}

validate_and_import_legacy_target() {
  local evidence="$1" suite="$2" lemma="$3" target_dir="$LOG_DIR/proofs/$suite/$lemma"
  local aggregate="$evidence/aggregate-$suite.tsv" raw="$evidence/proofs/$suite/$lemma.out"
  local exit_status recorded_status recorded_steps recorded_wf recorded_loop meta
  [[ -s "$aggregate" && -s "$raw" ]] || { echo "error: imported raw/aggregate missing for $suite/$lemma" >&2; return 1; }
  [[ "$(awk -F '\t' -v target="$lemma" 'NR>1 && $1==target {n++} END{print n+0}' "$aggregate")" -eq 1 ]] || return 1
  exit_status="$(legacy_aggregate_value "$aggregate" "$lemma" exit_status)"
  recorded_status="$(legacy_aggregate_value "$aggregate" "$lemma" status)"
  recorded_steps="$(legacy_aggregate_value "$aggregate" "$lemma" steps)"
  recorded_wf="$(legacy_aggregate_value "$aggregate" "$lemma" wellformedness)"
  recorded_loop="$(legacy_aggregate_value "$aggregate" "$lemma" loop_marker)"
  [[ "$exit_status" =~ ^[0-9]+$ ]] || return 1
  meta="$TMP_DIR/legacy-$suite-$lemma.tsv"; classify_attempt "$lemma" "$exit_status" "$raw" "$meta"
  [[ "$(attempt_field "$meta" status)" == "$recorded_status" \
     && "$(attempt_field "$meta" steps)" == "$recorded_steps" \
     && "$(attempt_field "$meta" wellformedness)" == "$recorded_wf" \
     && "$(attempt_field "$meta" loop_marker)" == "$recorded_loop" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" source_file)" == "proofs/$suite/$lemma.out" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" raw_result)" == "$(attempt_field "$meta" raw_result)" ]] || {
    echo "error: imported raw disagrees with aggregate for $suite/$lemma" >&2; return 1;
  }
  mkdir -p "$target_dir"
  cp "$raw" "$target_dir/attempt-1.out"
  printf '%s\n' "$exit_status" > "$target_dir/attempt-1.exit"
  printf 'imported\n' > "$target_dir/attempt-1.origin"
  cp "$meta" "$target_dir/attempt-1.meta.tsv"
}

validate_and_import_attempt_target() {
  local evidence="$1" suite="$2" lemma="$3" source_dir="$evidence/proofs/$suite/$lemma"
  local target_dir="$LOG_DIR/proofs/$suite/$lemma" raw attempt exit_status meta_tmp origin
  local expected_attempt=1 selected="-" selected_meta="" status steps wf loop timeout_marker count detail selected_origin reused
  local terminal_status="" current_status aggregate="$evidence/aggregate-$suite.tsv"
  local -a raws=() terminal_attempts=()
  shopt -s nullglob; raws=("$source_dir"/attempt-*.out); shopt -u nullglob
  [[ "${#raws[@]}" -gt 0 && "${#raws[@]}" -le "$MAX_ATTEMPTS" ]] || return 1
  mkdir -p "$target_dir"
  mapfile -t raws < <(printf '%s\n' "${raws[@]}" | LC_ALL=C sort -V)
  for raw in "${raws[@]}"; do
    attempt="${raw##*/attempt-}"; attempt="${attempt%.out}"
    [[ "$attempt" == "$expected_attempt" ]] || return 1; expected_attempt=$((expected_attempt + 1))
    [[ -s "$source_dir/attempt-$attempt.exit" && -s "$source_dir/attempt-$attempt.meta.tsv" \
       && -s "$source_dir/attempt-$attempt.origin" ]] || return 1
    exit_status="$(tr -d '\r\n' < "$source_dir/attempt-$attempt.exit")"
    origin="$(tr -d '\r\n' < "$source_dir/attempt-$attempt.origin")"
    [[ "$origin" == imported || "$origin" == executed-by-current-runner ]] || return 1
    meta_tmp="$TMP_DIR/import-attempt-$suite-$lemma-$attempt.tsv"
    classify_attempt "$lemma" "$exit_status" "$raw" "$meta_tmp"
    cmp -s "$meta_tmp" "$source_dir/attempt-$attempt.meta.tsv" || return 1
    if [[ "$(attempt_field "$meta_tmp" terminal)" == true ]]; then
      current_status="$(attempt_field "$meta_tmp" status)"
      [[ -z "$terminal_status" || "$terminal_status" == "$current_status" ]] || return 1
      terminal_status="$current_status"; terminal_attempts+=("$attempt")
    fi
    cp "$raw" "$target_dir/attempt-$attempt.out"
    cp "$source_dir/attempt-$attempt.exit" "$target_dir/attempt-$attempt.exit"
    cp "$meta_tmp" "$target_dir/attempt-$attempt.meta.tsv"
    printf 'imported\n' > "$target_dir/attempt-$attempt.origin"
  done
  count="${#raws[@]}"
  if [[ "${#terminal_attempts[@]}" -gt 0 ]]; then
    selected="${terminal_attempts[0]}"; selected_meta="$source_dir/attempt-$selected.meta.tsv"
    [[ -s "$source_dir/selected-attempt.txt" && "$(tr -d '\r\n' < "$source_dir/selected-attempt.txt")" == "$selected" ]] || return 1
  else
    [[ ! -e "$source_dir/selected-attempt.txt" ]] || return 1
    selected_meta="$source_dir/attempt-$count.meta.tsv"
  fi
  status="$(attempt_field "$selected_meta" status)"; steps="$(attempt_field "$selected_meta" steps)"
  exit_status="$(attempt_field "$selected_meta" exit_status)"; wf="$(attempt_field "$selected_meta" wellformedness)"
  loop="$(attempt_field "$selected_meta" loop_marker)"; timeout_marker="$(attempt_field "$selected_meta" timeout_marker)"
  detail="$(attempt_field "$selected_meta" raw_result)"
  if [[ "$selected" == - ]]; then reused=false; else
    selected_origin="$(tr -d '\r\n' < "$source_dir/attempt-$selected.origin")"
    [[ "$selected_origin" == imported ]] && reused=true || reused=false
  fi
  [[ "$(legacy_aggregate_value "$aggregate" "$lemma" status)" == "$status" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" steps)" == "$steps" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" exit_status)" == "$exit_status" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" wellformedness)" == "$wf" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" loop_marker)" == "$loop" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" timeout_marker)" == "$timeout_marker" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" attempt_count)" == "$count" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" selected_attempt)" == "$selected" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" reused)" == "$reused" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" source_directory)" == "proofs/$suite/$lemma" \
     && "$(legacy_aggregate_value "$aggregate" "$lemma" raw_result)" == "$detail" ]] || return 1
}

import_suite_attempts() {
  local evidence="$1" suite="$2" names_var="$3" expected_var="$4"
  local -n names_ref="$names_var" expected_ref="$expected_var"
  local lemma actual expected match vector="$evidence/result-vector-comparison.tsv"
  [[ "$(awk 'END{print NR+0}' "$evidence/aggregate-$suite.tsv")" -eq $((${#names_ref[@]} + 1)) ]] || return 1
  [[ "$(awk -F '\t' -v s="$suite" 'NR>1 && $1==s {n++} END{print n+0}' "$vector")" -eq "${#names_ref[@]}" ]] || return 1
  for lemma in "${names_ref[@]}"; do
    if [[ -d "$evidence/proofs/$suite/$lemma" ]]; then
      validate_and_import_attempt_target "$evidence" "$suite" "$lemma" || return 1
      actual="$(legacy_aggregate_value "$evidence/aggregate-$suite.tsv" "$lemma" status)"
    else
      validate_and_import_legacy_target "$evidence" "$suite" "$lemma" || return 1
      actual="$(legacy_aggregate_value "$evidence/aggregate-$suite.tsv" "$lemma" status)"
    fi
    expected="${expected_ref[$lemma]}"; [[ "$actual" == "$expected" ]] && match=MATCH || match=MISMATCH
    [[ "$(awk -F '\t' -v s="$suite" -v l="$lemma" -v a="$actual" -v e="$expected" -v m="$match" \
      '$1==s && $2==l && $3==a && $4==e && $5==m {n++} END{print n+0}' "$vector")" -eq 1 ]] || {
      echo "error: imported result vector disagrees for $suite/$lemma" >&2; return 1;
    }
  done
}

validate_imported_summary() {
  local evidence="$1" summary="$evidence/summary.txt" versions="$evidence/versions.txt"
  local source_head source_tree row suite field mismatches expected_status recorded_status errors=0
  local -a mappings=(
    'fixed-replay|fixed_replay_status'
    'fixed-impact|fixed_impact_status'
    'original-replay|original_replay_regression_status'
    'hmac-replay|hmac_replay_regression_status'
    'original-impact|original_impact_regression_status'
    'v6|v6_regression_status'
    'v7|v7_regression_status'
  )
  [[ -s "$summary" && -s "$evidence/result-vector-comparison.tsv" ]] || return 1
  source_head="$(awk -F ': ' '$1=="git_head" {print $2; exit}' "$versions")"
  source_tree="$(awk -F ': ' '$1=="git_tree" {print $2; exit}' "$versions")"
  [[ "$(awk -F ': ' '$1=="git_head" {print $2; exit}' "$summary")" == "$source_head" ]] || errors=1
  [[ "$(awk -F ': ' '$1=="git_tree" {print $2; exit}' "$summary")" == "$source_tree" ]] || errors=1
  for field in parse_fixed_replay_status parse_fixed_impact_status proverif_regression_status \
    formula_comparison_status constructor_comparison_status consumer_rule_comparison_status trace_status; do
    [[ "$(awk -F ': ' -v f="$field" '$1==f {print $2; exit}' "$summary")" == 0 ]] || errors=1
  done
  [[ "$(awk -F ': ' '$1=="post_run_unexpected_status_empty" {print $2; exit}' "$summary")" == true ]] || errors=1
  for row in "${mappings[@]}"; do
    IFS='|' read -r suite field <<< "$row"
    mismatches="$(awk -F '\t' -v s="$suite" 'NR>1 && $1==s && $5=="MISMATCH" {n++} END{print n+0}' "$evidence/result-vector-comparison.tsv")"
    [[ "$mismatches" -eq 0 ]] && expected_status=0 || expected_status=1
    recorded_status="$(awk -F ': ' -v f="$field" '$1==f {print $2; exit}' "$summary")"
    [[ "$recorded_status" == "$expected_status" ]] || errors=1
  done
  [[ "$errors" -eq 0 ]] || { echo "error: imported summary disagrees with imported results" >&2; return 1; }
}

validate_and_import_evidence() {
  local evidence="$1" manifest_check="$TMP_DIR/import-manifest-check.txt"
  local destination="$LOG_DIR" staging="$TMP_DIR/import-staging" import_status=0
  manifest_is_valid "$evidence" "$manifest_check" || { echo "error: imported SHA256SUMS validation failed" >&2; return 1; }
  validate_legacy_binding "$evidence" || return 1
  check_wellformedness_success "$evidence/parse/fixed-replay.out" || return 1
  check_wellformedness_success "$evidence/parse/fixed-impact.out" || return 1
  ! grep -Fq '<<loop>>' "$evidence/parse/fixed-replay.out" || return 1
  ! grep -Fq '<<loop>>' "$evidence/parse/fixed-impact.out" || return 1
  validate_imported_comparisons "$evidence" || return 1
  validate_imported_proverif "$evidence" || return 1
  validate_imported_traces "$evidence" || return 1

  LOG_DIR="$staging"
  mkdir -p "$LOG_DIR/imported-run" "$LOG_DIR/proofs"
  cp -a "$evidence/." "$LOG_DIR/imported-run/"
  cp -a "$evidence/parse" "$LOG_DIR/"
  cp -a "$evidence/regressions" "$LOG_DIR/"
  cp -a "$evidence/traces" "$LOG_DIR/"
  cp "$evidence/proverif-result-comparison.tsv" "$LOG_DIR/"
  import_suite_attempts "$evidence" fixed-replay FIXED_REPLAY_LEMMAS FIXED_REPLAY_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" fixed-impact FIXED_IMPACT_LEMMAS FIXED_IMPACT_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" original-replay REPLAY_FROZEN ORIGINAL_REPLAY_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" hmac-replay HMAC_REPLAY_LEMMAS HMAC_REPLAY_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" original-impact ORIGINAL_IMPACT_LEMMAS ORIGINAL_IMPACT_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" v6 V6_LEMMAS V6_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && import_suite_attempts "$evidence" v7 V7_LEMMAS V7_EXPECTED || import_status=1
  [[ "$import_status" -eq 0 ]] && validate_imported_summary "$evidence" || import_status=1
  if [[ "$import_status" -eq 0 ]]; then
    cp "$manifest_check" "$staging/imported-manifest-validation.out"
    {
      echo "resume_source: $evidence"
      echo "source_manifest_sha256: $(sha256sum "$evidence/SHA256SUMS.txt" | awk '{print $1}')"
      echo "source_manifest_valid: true"
      echo "execution_head_tree_valid: true"
      echo "input_blob_sha256_bindings_valid: true"
      echo "tool_versions_match: true"
      echo "aggregate_raw_results_valid: true"
      echo "formula_constructor_consumer_valid: true"
      echo "proverif_results_valid: true"
      echo "trace_results_valid: true"
      echo "summary_consistent: true"
      echo "proof_targets_imported: 196"
    } > "$staging/import-validation.txt"
  fi
  LOG_DIR="$destination"
  [[ "$import_status" -eq 0 ]] || return 1
  mkdir -p "$LOG_DIR"
  cp -a "$staging/." "$LOG_DIR/"
}

capture_tool_binding() {
  local destination="$1" tamarin_file="$TMP_DIR/tamarin-version-current.txt" proverif_file="$TMP_DIR/proverif-version-current.txt"
  local tamarin_version maude_version proverif_version pv_status
  tamarin-prover --version > "$tamarin_file" 2>&1
  tamarin_version="$(grep -m1 '^Tamarin version ' "$tamarin_file" | sed 's/^Tamarin version //')"
  maude_version="$(maude --version 2>&1 | sed -n '1{s/\r$//;p;}')"
  set +e; "${PROVERIF_CMD[@]}" -version > "$proverif_file" 2>&1; pv_status=$?; set -e
  proverif_version="$(grep -m1 '^Proverif [0-9]' "$proverif_file" | awk '{print $2}' | tr -d '.')"
  [[ -n "$tamarin_version" && -n "$maude_version" && -n "$proverif_version" ]] || return 1
  {
    printf 'tool\tversion\n'
    printf 'tamarin-prover\t%s\n' "$tamarin_version"
    printf 'maude\t%s\n' "$maude_version"
    printf 'proverif\t%s\n' "$proverif_version"
    printf 'proverif-version-command-exit\t%s\n' "$pv_status"
  } > "$destination"
}

write_evidence_binding() {
  local destination="$1" path
  {
    printf 'record\tpath_or_name\tvalue1\tvalue2\n'
    printf 'execution\thead\t%s\t-\n' "$GIT_HEAD"
    printf 'execution\ttree\t%s\t-\n' "$GIT_TREE"
    printf 'execution\tbranch\t%s\t-\n' "$GIT_BRANCH"
    for path in "${TRACKED_INPUTS[@]}"; do
      printf 'input\t%s\t%s\t%s\n' "$path" \
        "$("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$path")" "$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    done
  } > "$destination"
}

validate_evidence_binding_file() {
  local evidence="$1" binding="$evidence/evidence-binding.tsv" recorded_head recorded_tree actual_tree
  local path blob sha object_file object_sha
  [[ -s "$binding" && -s "$evidence/tool-binding.tsv" ]] || return 1
  [[ "$(awk -F '\t' '
    NR==1 && $1=="tool" && $2=="version" {header=1; next}
    $1=="tamarin-prover" && $2!="" {t++}
    $1=="maude" && $2!="" {m++}
    $1=="proverif" && $2!="" {p++}
    $1=="proverif-version-command-exit" && $2 ~ /^[0-9]+$/ {e++}
    END {print (header && t==1 && m==1 && p==1 && e==1 && NR==5) ? "valid" : "invalid"}
  ' "$evidence/tool-binding.tsv")" == valid ]] || return 1
  recorded_head="$(awk -F '\t' '$1=="execution" && $2=="head" {print $3}' "$binding")"
  recorded_tree="$(awk -F '\t' '$1=="execution" && $2=="tree" {print $3}' "$binding")"
  [[ "$recorded_head" =~ ^[0-9a-f]{40}$ && "$recorded_tree" =~ ^[0-9a-f]{40}$ ]] || return 1
  actual_tree="$("${GIT_CMD[@]}" show -s --format=%T "$recorded_head")"
  [[ "$actual_tree" == "$recorded_tree" ]] || return 1
  for path in "${TRACKED_INPUTS[@]}"; do
    blob="$(awk -F '\t' -v p="$path" '$1=="input" && $2==p {print $3}' "$binding")"
    sha="$(awk -F '\t' -v p="$path" '$1=="input" && $2==p {print $4}' "$binding")"
    [[ "$("${GIT_CMD[@]}" rev-parse "$recorded_head:$path")" == "$blob" ]] || return 1
    object_file="$TMP_DIR/verify-object-${RANDOM}"; "${GIT_CMD[@]}" cat-file blob "$recorded_head:$path" > "$object_file"
    object_sha="$(sha256sum "$object_file" | awk '{print $1}')"; [[ "$object_sha" == "$sha" ]] || return 1
    [[ "$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')" == "$sha" ]] || return 1
  done
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

verify_suite_results() {
  local suite="$1" model_rel="$2" names_var="$3" expected_var="$4"
  local -n names_ref="$names_var"
  local rebuilt="$TMP_DIR/rebuilt-aggregate-$suite.tsv" lemma errors=0
  printf 'lemma\tstatus\tsteps\texit_status\twellformedness\tloop_marker\ttimeout_marker\tattempt_count\tselected_attempt\treused\tsource_directory\traw_result\n' > "$rebuilt"
  for lemma in "${names_ref[@]}"; do
    evaluate_target_attempts "$suite" "$lemma" "$model_rel" "$rebuilt" false true || errors=1
  done
  cmp -s "$rebuilt" "$LOG_DIR/aggregate-$suite.tsv" || errors=1
  validate_suite "$suite" "$rebuilt" "$names_var" "$expected_var" || errors=1
  return "$errors"
}

verify_final_package() {
  local evidence="$1" original_log_dir="$LOG_DIR" errors=0
  local rebuilt_attempt_count rebuilt_terminal rebuilt_loops rebuilt_timeouts rebuilt_reused
  LOG_DIR="$evidence"
  COMMAND_LOG="$LOG_DIR/command.txt"; VERSIONS_LOG="$LOG_DIR/versions.txt"; SUMMARY_LOG="$LOG_DIR/summary.txt"
  RESULT_VECTOR_LOG="$TMP_DIR/rebuilt-result-vector.tsv"; ATTEMPT_SUMMARY_LOG="$TMP_DIR/rebuilt-attempt-summary.tsv"
  printf 'suite\tlemma\tactual_status\texpected_status\tmatch\n' > "$RESULT_VECTOR_LOG"
  printf 'suite\tlemma\tattempt\texit_status\tstatus\twellformedness\tloop_marker\ttimeout_marker\tterminal\tretry_eligible\torigin\traw_output\n' > "$ATTEMPT_SUMMARY_LOG"
  manifest_is_valid "$evidence" "$TMP_DIR/verify-manifest.txt" || errors=1
  validate_evidence_binding_file "$evidence" || errors=1
  if grep -q '^runner_mode: resume$' "$evidence/summary.txt"; then
    [[ -s "$evidence/import-validation.txt" && -d "$evidence/imported-run" ]] || errors=1
    grep -q '^aggregate_raw_results_valid: true$' "$evidence/import-validation.txt" || errors=1
    manifest_is_valid "$evidence/imported-run" "$TMP_DIR/verify-imported-manifest.txt" || errors=1
  fi
  check_wellformedness_success "$evidence/parse/fixed-replay.out" || errors=1
  check_wellformedness_success "$evidence/parse/fixed-impact.out" || errors=1
  validate_imported_comparisons "$evidence" || errors=1
  validate_imported_proverif "$evidence" || errors=1
  validate_imported_traces "$evidence" || errors=1
  verify_suite_results fixed-replay "$FIXED_REPLAY_REL" FIXED_REPLAY_LEMMAS FIXED_REPLAY_EXPECTED || errors=1
  verify_suite_results fixed-impact "$FIXED_IMPACT_REL" FIXED_IMPACT_LEMMAS FIXED_IMPACT_EXPECTED || errors=1
  verify_suite_results original-replay "$ORIGINAL_REPLAY_REL" REPLAY_FROZEN ORIGINAL_REPLAY_EXPECTED || errors=1
  verify_suite_results hmac-replay "$HMAC_REPLAY_REL" HMAC_REPLAY_LEMMAS HMAC_REPLAY_EXPECTED || errors=1
  verify_suite_results original-impact "$ORIGINAL_IMPACT_REL" ORIGINAL_IMPACT_LEMMAS ORIGINAL_IMPACT_EXPECTED || errors=1
  verify_suite_results v6 "$V6_REL" V6_LEMMAS V6_EXPECTED || errors=1
  verify_suite_results v7 "$V7_REL" V7_LEMMAS V7_EXPECTED || errors=1
  cmp -s "$RESULT_VECTOR_LOG" "$evidence/result-vector-comparison.tsv" || errors=1
  cmp -s "$ATTEMPT_SUMMARY_LOG" "$evidence/attempt-summary.tsv" || errors=1
  awk 'found {print} /^attempt_details:$/ {found=1}' "$evidence/summary.txt" > "$TMP_DIR/summary-attempt-details.tsv"
  cmp -s "$ATTEMPT_SUMMARY_LOG" "$TMP_DIR/summary-attempt-details.tsv" || errors=1
  [[ "$(awk -F '\t' 'NR>1 && $5=="MISMATCH" {n++} END{print n+0}' "$RESULT_VECTOR_LOG")" -eq 0 ]] || errors=1
  [[ "$(awk -F '\t' 'NR>1 {n++} END{print n+0}' "$RESULT_VECTOR_LOG")" -eq 196 ]] || errors=1
  rebuilt_attempt_count="$(awk -F '\t' 'NR>1 {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
  rebuilt_terminal="$(awk -F '\t' 'NR>1 && $9=="true" {seen[$1 FS $2]=1} END{for(k in seen)n++; print n+0}' "$ATTEMPT_SUMMARY_LOG")"
  rebuilt_loops="$(awk -F '\t' 'NR>1 && $7=="true" {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
  rebuilt_timeouts="$(awk -F '\t' 'NR>1 && $8=="true" {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
  rebuilt_reused="$(awk -F '\t' 'NR>1 && $11=="imported" && $9=="true" {seen[$1 FS $2]=1} END{for(k in seen)n++; print n+0}' "$ATTEMPT_SUMMARY_LOG")"
  [[ "$rebuilt_terminal" -eq 196 ]] || errors=1
  [[ "$(awk -F ': ' '$1=="planned_targets" {print $2; exit}' "$evidence/summary.txt")" == 196 ]] || errors=1
  [[ "$(awk -F ': ' '$1=="attempt_count" {print $2; exit}' "$evidence/summary.txt")" == "$rebuilt_attempt_count" ]] || errors=1
  [[ "$(awk -F ': ' '$1=="terminal_targets" {print $2; exit}' "$evidence/summary.txt")" == "$rebuilt_terminal" ]] || errors=1
  [[ "$(awk -F ': ' '$1=="loop_attempt_count" {print $2; exit}' "$evidence/summary.txt")" == "$rebuilt_loops" ]] || errors=1
  [[ "$(awk -F ': ' '$1=="timeout_attempt_count" {print $2; exit}' "$evidence/summary.txt")" == "$rebuilt_timeouts" ]] || errors=1
  [[ "$(awk -F ': ' '$1=="reused_terminal_targets" {print $2; exit}' "$evidence/summary.txt")" == "$rebuilt_reused" ]] || errors=1
  if [[ "$rebuilt_loops" -gt 0 ]]; then
    grep -q '^intermittent_loop_observed: true$' "$evidence/summary.txt" || errors=1
  else
    grep -q '^intermittent_loop_observed: false$' "$evidence/summary.txt" || errors=1
  fi
  grep -q '^all_196_targets_terminal: true$' "$evidence/summary.txt" || errors=1
  grep -q '^all_result_vectors_match: true$' "$evidence/summary.txt" || errors=1
  LOG_DIR="$original_log_dir"
  [[ "$errors" -eq 0 ]] || { echo "error: evidence verification failed" >&2; return 1; }
  echo "VERIFY_ONLY_OK: $evidence"
}

run_synthetic_self_test() {
  local test_root="$TMP_DIR/synthetic-evidence" target="$TMP_DIR/synthetic-evidence/proofs/test/demo"
  local aggregate="$TMP_DIR/synthetic-aggregate.tsv" falsified_raw="$TMP_DIR/falsified.out" falsified_meta="$TMP_DIR/falsified.meta"
  LOG_DIR="$test_root"; COMMAND_LOG="$test_root/command.txt"; ATTEMPT_SUMMARY_LOG="$test_root/attempt-summary.tsv"
  mkdir -p "$target"; : > "$COMMAND_LOG"
  printf 'suite\tlemma\tattempt\texit_status\tstatus\twellformedness\tloop_marker\ttimeout_marker\tterminal\tretry_eligible\torigin\traw_output\n' > "$ATTEMPT_SUMMARY_LOG"
  printf 'tamarin-prover: <<loop>>\n' > "$target/attempt-1.out"
  printf '1\n' > "$target/attempt-1.exit"; printf 'imported\n' > "$target/attempt-1.origin"
  classify_attempt demo 1 "$target/attempt-1.out" "$target/attempt-1.meta.tsv"
  {
    printf '/* All wellformedness checks were successful. */\n'
    printf 'summary of summaries:\n'
    printf '  demo (all-traces): verified (3 steps)\n'
  } > "$target/attempt-2.out"
  printf '0\n' > "$target/attempt-2.exit"; printf 'imported\n' > "$target/attempt-2.origin"
  classify_attempt demo 0 "$target/attempt-2.out" "$target/attempt-2.meta.tsv"
  printf 'lemma\tstatus\tsteps\texit_status\twellformedness\tloop_marker\ttimeout_marker\tattempt_count\tselected_attempt\treused\tsource_directory\traw_result\n' > "$aggregate"
  evaluate_target_attempts test demo synthetic.spthy "$aggregate" false false
  [[ "$(legacy_aggregate_value "$aggregate" demo status)" == verified ]] || return 1
  [[ "$(legacy_aggregate_value "$aggregate" demo attempt_count)" == 2 ]] || return 1
  [[ "$(legacy_aggregate_value "$aggregate" demo selected_attempt)" == 2 ]] || return 1
  [[ -s "$target/attempt-1.out" && -s "$target/attempt-2.out" ]] || return 1

  {
    printf '/* All wellformedness checks were successful. */\n'
    printf 'summary of summaries:\n'
    printf '  demo (exists-trace): falsified - found trace (4 steps)\n'
  } > "$falsified_raw"
  classify_attempt demo 0 "$falsified_raw" "$falsified_meta"
  [[ "$(attempt_field "$falsified_meta" terminal)" == true ]] || return 1
  [[ "$(attempt_field "$falsified_meta" retry_eligible)" == false ]] || return 1

  cp "$falsified_raw" "$target/attempt-3.out"; printf '0\n' > "$target/attempt-3.exit"; printf 'imported\n' > "$target/attempt-3.origin"
  cp "$falsified_meta" "$target/attempt-3.meta.tsv"
  : > "$aggregate"
  if evaluate_target_attempts test demo synthetic.spthy "$aggregate" false true 2>/dev/null; then
    echo "error: inconsistent terminal attempts were accepted" >&2; return 1
  fi
  echo "SYNTHETIC_SELF_TEST_OK"
}

if [[ "$MODE" == self-test ]]; then
  run_synthetic_self_test
  exit $?
fi

if [[ "$MODE" == verify ]]; then
  verify_final_package "$SOURCE_EVIDENCE"
  exit $?
fi

if [[ "$MODE" == resume ]]; then
  validate_and_import_evidence "$SOURCE_EVIDENCE" || {
    echo "error: resume source validation failed before any proof invocation" >&2
    exit 2
  }
else
  mkdir -p "$LOG_DIR/parse" "$LOG_DIR/proofs" "$LOG_DIR/regressions" "$LOG_DIR/traces"
fi

printf 'suite\tlemma\tactual_status\texpected_status\tmatch\n' > "$RESULT_VECTOR_LOG"
printf 'suite\tlemma\tattempt\texit_status\tstatus\twellformedness\tloop_marker\ttimeout_marker\tterminal\tretry_eligible\torigin\traw_output\n' > "$ATTEMPT_SUMMARY_LOG"
printf 'scope\tlemma\tsource_sha256\tfixed_sha256\tmatch\n' > "$FORMULA_LOG"
printf 'scope\tsource_sha256\tfixed_sha256\tmatch\n' > "$CONSTRUCTOR_LOG"
if [[ "$MODE" == fresh ]]; then
  printf 'suite\ttarget\texit_status\tresult_vector_match\traw_output\n' > "$LOG_DIR/proverif-result-comparison.tsv"
fi

{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "working_directory: $ROOT_DIR"
  echo "runner_mode: $MODE"
  [[ "$MODE" == resume ]] && echo "validated_resume_source: $SOURCE_EVIDENCE"
  print_command parse_fixed_replay tamarin-prover --parse-only "$FIXED_REPLAY_REL"
  print_command parse_fixed_impact tamarin-prover --parse-only "$FIXED_IMPACT_REL"
} > "$COMMAND_LOG"

write_evidence_binding "$BINDING_LOG"
capture_tool_binding "$TOOL_BINDING_LOG"
{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "utc_start: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "git_branch: $GIT_BRANCH"
  echo "git_head: $GIT_HEAD"
  echo "git_tree: $GIT_TREE"
  echo "execution_mode: bounded_attempts_per_exact_lemma"
  echo "runner_mode: $MODE"
  echo "max_attempts_per_target: $MAX_ATTEMPTS"
  echo "proof_timeout_seconds: $PROOF_TIMEOUT_SECONDS"
  [[ "$MODE" == resume ]] && echo "validated_resume_source: $SOURCE_EVIDENCE"
  echo "clean_pre_run_status: true"
  echo "tracked_input_metadata:"
  for path in "${TRACKED_INPUTS[@]}"; do
    echo "path: $path"
    echo "  blob_oid: $("${GIT_CMD[@]}" rev-parse "$GIT_HEAD:$path")"
    echo "  sha256: $(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    echo "  eol: $(detect_eol "$ROOT_DIR/$path")"
  done
  echo "git_check_attr_output:"
  "${GIT_CMD[@]}" check-attr text eol -- "${TRACKED_INPUTS[@]}"
  echo; echo "tamarin-prover --version:"; tamarin-prover --version
  echo; echo "maude --version:"; maude --version
  echo; echo "proverif version:"; "${PROVERIF_CMD[@]}" -version 2>&1 || true
} > "$VERSIONS_LOG" 2>&1

formula_status=0
compare_formula_set replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" "$ROOT_DIR/$FIXED_REPLAY_REL" REPLAY_FROZEN || formula_status=1
compare_formula_set impact-composition "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" IMPACT_COMPOSITION || formula_status=1
compare_formula_set impact-lower "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" REPLAY_FROZEN || formula_status=1
constructor_status=0
compare_constructors replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" "$ROOT_DIR/$FIXED_REPLAY_REL" || constructor_status=1
compare_constructors impact "$ROOT_DIR/$ORIGINAL_IMPACT_REL" "$ROOT_DIR/$FIXED_IMPACT_REL" || constructor_status=1
consumer_rule_status=0
compare_consumer_rules || consumer_rule_status=1

cd "$ROOT_DIR"
parse_fixed_replay_status=0; parse_fixed_impact_status=0
if [[ "$MODE" == fresh ]]; then
  tamarin-prover --parse-only "$FIXED_REPLAY_REL" > "$LOG_DIR/parse/fixed-replay.out" 2>&1 || parse_fixed_replay_status=$?
  tamarin-prover --parse-only "$FIXED_IMPACT_REL" > "$LOG_DIR/parse/fixed-impact.out" 2>&1 || parse_fixed_impact_status=$?
else
  check_wellformedness_success "$LOG_DIR/parse/fixed-replay.out" || parse_fixed_replay_status=1
  check_wellformedness_success "$LOG_DIR/parse/fixed-impact.out" || parse_fixed_impact_status=1
fi
check_wellformedness_success "$LOG_DIR/parse/fixed-replay.out" || parse_fixed_replay_status=1
check_wellformedness_success "$LOG_DIR/parse/fixed-impact.out" || parse_fixed_impact_status=1
! grep -Fq '<<loop>>' "$LOG_DIR/parse/fixed-replay.out" || parse_fixed_replay_status=1
! grep -Fq '<<loop>>' "$LOG_DIR/parse/fixed-impact.out" || parse_fixed_impact_status=1

fixed_replay_status=0; fixed_impact_status=0; original_replay_status=0
hmac_replay_status=0; original_impact_status=0; v6_status=0; v7_status=0
run_tamarin_suite fixed-replay "$FIXED_REPLAY_REL" FIXED_REPLAY_LEMMAS FIXED_REPLAY_EXPECTED || fixed_replay_status=1
run_tamarin_suite fixed-impact "$FIXED_IMPACT_REL" FIXED_IMPACT_LEMMAS FIXED_IMPACT_EXPECTED || fixed_impact_status=1
run_tamarin_suite original-replay "$ORIGINAL_REPLAY_REL" REPLAY_FROZEN ORIGINAL_REPLAY_EXPECTED || original_replay_status=1
run_tamarin_suite hmac-replay "$HMAC_REPLAY_REL" HMAC_REPLAY_LEMMAS HMAC_REPLAY_EXPECTED || hmac_replay_status=1
run_tamarin_suite original-impact "$ORIGINAL_IMPACT_REL" ORIGINAL_IMPACT_LEMMAS ORIGINAL_IMPACT_EXPECTED || original_impact_status=1
run_tamarin_suite v6 "$V6_REL" V6_LEMMAS V6_EXPECTED || v6_status=1
run_tamarin_suite v7 "$V7_REL" V7_LEMMAS V7_EXPECTED || v7_status=1

proverif_status=0; trace_status=0
if [[ "$MODE" == fresh ]]; then
  run_proverif_target proverif-original BASELINE "$PROVERIF_ORIGINAL_REL" "$PROVERIF_ORIGINAL_BASELINE_REL" || proverif_status=1
  run_proverif_target proverif-original COMPONENT "$PROVERIF_ORIGINAL_REL" "$PROVERIF_ORIGINAL_BASELINE_REL" || proverif_status=1
  run_proverif_target proverif-hmac HMAC_BASELINE "$PROVERIF_HMAC_REL" "$PROVERIF_HMAC_BASELINE_REL" || proverif_status=1
  run_proverif_target proverif-hmac HMAC_COMPONENT "$PROVERIF_HMAC_REL" "$PROVERIF_HMAC_BASELINE_REL" || proverif_status=1
  run_trace duplicate-fail "$FIXED_REPLAY_REL" duplicate_batch_fail_exists || trace_status=1
  run_trace distinct-complete "$FIXED_REPLAY_REL" normal_distinct_batch_complete || trace_status=1
  run_trace distinct-fail-slot1 "$FIXED_REPLAY_REL" normal_distinct_fail_slot1_exists || trace_status=1
  run_trace distinct-fail-slot2 "$FIXED_REPLAY_REL" normal_distinct_fail_slot2_exists || trace_status=1
  run_trace distinct-consumer "$FIXED_IMPACT_REL" normal_distinct_consumer_complete || trace_status=1
else
  validate_imported_proverif "$LOG_DIR" || proverif_status=1
  validate_imported_traces "$LOG_DIR" || trace_status=1
fi

POST_RUN_GIT_STATUS="$("${GIT_CMD[@]}" status --porcelain=v1 --untracked-files=all)"
UNEXPECTED_STATUS="$(printf '%s\n' "$POST_RUN_GIT_STATUS" | awk -v prefix="?? $LOG_REL/" 'NF && index($0,prefix) != 1 {print}')"
planned_targets="$((${#FIXED_REPLAY_LEMMAS[@]} + ${#FIXED_IMPACT_LEMMAS[@]} + ${#REPLAY_FROZEN[@]} + ${#HMAC_REPLAY_LEMMAS[@]} + ${#ORIGINAL_IMPACT_LEMMAS[@]} + ${#V6_LEMMAS[@]} + ${#V7_LEMMAS[@]}))"
attempt_count="$(awk -F '\t' 'NR>1 {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
terminal_targets="$(awk -F '\t' 'NR>1 && $9=="true" {seen[$1 FS $2]=1} END{for(k in seen)n++; print n+0}' "$ATTEMPT_SUMMARY_LOG")"
loop_attempts="$(awk -F '\t' 'NR>1 && $7=="true" {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
timeout_attempts="$(awk -F '\t' 'NR>1 && $8=="true" {n++} END{print n+0}' "$ATTEMPT_SUMMARY_LOG")"
reused_targets="$(awk -F '\t' 'NR>1 && $11=="imported" && $9=="true" {seen[$1 FS $2]=1} END{for(k in seen)n++; print n+0}' "$ATTEMPT_SUMMARY_LOG")"
vector_mismatches="$(awk -F '\t' 'NR>1 && $5=="MISMATCH" {n++} END{print n+0}' "$RESULT_VECTOR_LOG")"
{
  echo "K-Waay M3 batch-local atomic dedup evidence summary"
  echo "git_head: $GIT_HEAD"; echo "git_tree: $GIT_TREE"; echo "runner_mode: $MODE"
  echo "max_attempts_per_target: $MAX_ATTEMPTS"; echo "proof_timeout_seconds: $PROOF_TIMEOUT_SECONDS"
  echo "planned_targets: $planned_targets"; echo "attempt_count: $attempt_count"; echo "terminal_targets: $terminal_targets"
  echo "loop_attempt_count: $loop_attempts"; echo "timeout_attempt_count: $timeout_attempts"
  echo "intermittent_loop_observed: $([[ "$loop_attempts" -gt 0 ]] && echo true || echo false)"
  echo "reused_terminal_targets: $reused_targets"
  echo "all_196_targets_terminal: $([[ "$terminal_targets" -eq 196 ]] && echo true || echo false)"
  echo "all_result_vectors_match: $([[ "$vector_mismatches" -eq 0 ]] && echo true || echo false)"
  echo "parse_fixed_replay_status: $parse_fixed_replay_status"; echo "parse_fixed_impact_status: $parse_fixed_impact_status"
  echo "fixed_replay_status: $fixed_replay_status"; echo "fixed_impact_status: $fixed_impact_status"
  echo "original_replay_regression_status: $original_replay_status"; echo "hmac_replay_regression_status: $hmac_replay_status"
  echo "original_impact_regression_status: $original_impact_status"; echo "v6_regression_status: $v6_status"; echo "v7_regression_status: $v7_status"
  echo "proverif_regression_status: $proverif_status"; echo "formula_comparison_status: $formula_status"
  echo "constructor_comparison_status: $constructor_status"; echo "consumer_rule_comparison_status: $consumer_rule_status"
  echo "trace_status: $trace_status"
  echo "post_run_unexpected_status_empty: $([[ -z "$UNEXPECTED_STATUS" ]] && echo true || echo false)"
  echo "attempt_details_file: attempt-summary.tsv"
  echo "attempt_details:"; cat "$ATTEMPT_SUMMARY_LOG"
} > "$SUMMARY_LOG"

{
  echo; echo "utc_end: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"; cat "$SUMMARY_LOG"
  echo "post_run_git_status:"; printf '%s\n' "$POST_RUN_GIT_STATUS"
} >> "$VERSIONS_LOG"

(
  cd "$LOG_DIR"
  find . -type f ! -path './SHA256SUMS.txt' -printf '%P\0' | LC_ALL=C sort -z | xargs -0 sha256sum
) > "$MANIFEST_LOG"

cat "$SUMMARY_LOG"
final_status=0
for status in "$parse_fixed_replay_status" "$parse_fixed_impact_status" "$fixed_replay_status" "$fixed_impact_status" \
  "$original_replay_status" "$hmac_replay_status" "$original_impact_status" "$v6_status" "$v7_status" \
  "$proverif_status" "$formula_status" "$constructor_status" "$consumer_rule_status" "$trace_status"; do
  [[ "$status" == 0 ]] || final_status=1
done
[[ "$planned_targets" -eq 196 && "$terminal_targets" -eq 196 && "$vector_mismatches" -eq 0 ]] || final_status=1
if [[ -n "$UNEXPECTED_STATUS" ]]; then
  echo "error: unexpected post-run worktree changes" >&2; printf '%s\n' "$UNEXPECTED_STATUS" >&2; final_status=1
fi
exit "$final_status"
