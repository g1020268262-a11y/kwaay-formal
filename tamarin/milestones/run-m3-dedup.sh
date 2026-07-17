#!/usr/bin/env bash

set -euo pipefail

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

if [[ -n "$PRE_RUN_GIT_STATUS" ]]; then
  echo "error: pre-run git status is not clean" >&2
  printf '%s\n' "$PRE_RUN_GIT_STATUS" >&2
  exit 2
fi
if [[ -e "$LOG_DIR" ]]; then
  echo "error: M3 evidence directory already exists: $LOG_DIR" >&2
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
if ! "${GIT_CMD[@]}" diff --quiet HEAD -- "${TRACKED_INPUTS[@]}"; then
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

for command_name in tamarin-prover maude cpp timeout sha256sum awk sed grep sort find xargs; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "error: required command not found: $command_name" >&2
    exit 2
  fi
done

PROVERIF_CMD=()
PROVERIF_NEEDS_WIN_PATH=0
if command -v proverif >/dev/null 2>&1; then
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

TAMARIN_HELP="$(tamarin-prover --help 2>&1)"
for option in --output-json --output-dot; do
  if ! grep -q -- "$option" <<<"$TAMARIN_HELP"; then
    echo "error: installed Tamarin does not advertise $option" >&2
    exit 2
  fi
done

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

analyze_selected_output() {
  local suite="$1" lemma="$2" exit_status="$3" raw_file="$4" source_rel="$5" aggregate="$6"
  local rows="$TMP_DIR/${suite}-${lemma}.tsv" status="missing" steps="-" detail="MISSING"
  local wellformedness="failure" loop_marker="false" errors=0 target_count other_terminal_count
  : > "$rows"
  if [[ -s "$raw_file" ]]; then
    extract_result_rows "$raw_file" > "$rows"
    target_count="$(awk -F '\t' -v target="$lemma" '$1 == target {n++} END {print n+0}' "$rows")"
    other_terminal_count="$(awk -F '\t' -v target="$lemma" '$1 != target && ($2 == "verified" || $2 == "falsified") {n++} END {print n+0}' "$rows")"
    if [[ "$target_count" -eq 1 ]]; then
      IFS=$'\t' read -r _ status steps detail < <(awk -F '\t' -v target="$lemma" '$1 == target {print; exit}' "$rows")
    else
      errors=1; detail="target-summary-count=$target_count"
    fi
    if check_wellformedness_success "$raw_file"; then wellformedness="success"; else errors=1; fi
    if grep -Fq '<<loop>>' "$raw_file"; then loop_marker="true"; errors=1; fi
    [[ "$other_terminal_count" -eq 0 ]] || errors=1
  else
    errors=1
  fi
  [[ "$exit_status" == 0 ]] || errors=1
  [[ "$status" == verified || "$status" == falsified ]] || errors=1
  detail="${detail//$'\t'/ }"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$lemma" "$status" "$steps" "$exit_status" "$wellformedness" "$loop_marker" "$source_rel" "$detail" >> "$aggregate"
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
  local lemma raw status suite_errors=0
  mkdir -p "$proof_dir"
  printf 'lemma\tstatus\tsteps\texit_status\twellformedness\tloop_marker\tsource_file\traw_result\n' > "$aggregate"
  for lemma in "${names_ref[@]}"; do
    raw="$proof_dir/$lemma.out"
    {
      print_command "executed-proof[$suite][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$model_rel"
      echo "raw_output[$suite][$lemma]: ${raw#"$ROOT_DIR/"}"
    } >> "$COMMAND_LOG"
    set +e
    tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$model_rel" > "$raw" 2>&1
    status=$?
    set -e
    if ! analyze_selected_output "$suite" "$lemma" "$status" "$raw" "proofs/$suite/$lemma.out" "$aggregate"; then suite_errors=1; fi
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
  local label="$1" source="$2" target="$3" a="$TMP_DIR/$label-functions-a" b="$TMP_DIR/$label-functions-b" match
  extract_functions_block "$source" "$a"; extract_functions_block "$target" "$b"
  if cmp -s "$a" "$b"; then match=MATCH; else match=MISMATCH; fi
  printf '%s\t%s\t%s\t%s\n' "$label" "$(sha256sum "$a" | awk '{print $1}')" "$(sha256sum "$b" | awk '{print $1}')" "$match" >> "$CONSTRUCTOR_LOG"
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
  local suite="$1" target="$2" model_rel="$3" baseline_rel="$4"
  local dir="$LOG_DIR/regressions/$suite" generated="$dir/generated/$target.pv" raw="$dir/$target.out" cpp_err="$dir/$target.cpp.err"
  local input status errors=0 actual="$TMP_DIR/$suite-$target-actual" baseline="$TMP_DIR/$suite-$target-baseline" match
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
  local label="$1" model_rel="$2" lemma="$3"
  local dir="$LOG_DIR/traces/$label" raw="$dir/trace.out" json="$dir/trace.json" dot="$dir/trace.dot" status errors=0
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

mkdir -p "$LOG_DIR/parse" "$LOG_DIR/proofs" "$LOG_DIR/regressions" "$LOG_DIR/traces"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

printf 'suite\tlemma\tactual_status\texpected_status\tmatch\n' > "$RESULT_VECTOR_LOG"
printf 'scope\tlemma\tsource_sha256\tfixed_sha256\tmatch\n' > "$FORMULA_LOG"
printf 'scope\tsource_sha256\tfixed_sha256\tmatch\n' > "$CONSTRUCTOR_LOG"
printf 'suite\ttarget\texit_status\tresult_vector_match\traw_output\n' > "$LOG_DIR/proverif-result-comparison.tsv"

{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "working_directory: $ROOT_DIR"
  print_command parse_fixed_replay tamarin-prover --parse-only "$FIXED_REPLAY_REL"
  print_command parse_fixed_impact tamarin-prover --parse-only "$FIXED_IMPACT_REL"
  for lemma in "${FIXED_REPLAY_LEMMAS[@]}"; do
    print_command "proof[fixed-replay][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$FIXED_REPLAY_REL"
  done
  for lemma in "${FIXED_IMPACT_LEMMAS[@]}"; do
    print_command "proof[fixed-impact][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$FIXED_IMPACT_REL"
  done
  for lemma in "${REPLAY_FROZEN[@]}"; do
    print_command "proof[original-replay][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$ORIGINAL_REPLAY_REL"
  done
  for lemma in "${HMAC_REPLAY_LEMMAS[@]}"; do
    print_command "proof[hmac-replay][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$HMAC_REPLAY_REL"
  done
  for lemma in "${ORIGINAL_IMPACT_LEMMAS[@]}"; do
    print_command "proof[original-impact][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$ORIGINAL_IMPACT_REL"
  done
  for lemma in "${V6_LEMMAS[@]}"; do
    print_command "proof[v6][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$V6_REL"
  done
  for lemma in "${V7_LEMMAS[@]}"; do
    print_command "proof[v7][$lemma]" tamarin-prover --derivcheck-timeout=0 "--prove=$lemma" "$V7_REL"
  done
  print_command 'proverif[original][BASELINE]' cpp -P -D BASELINE "$PROVERIF_ORIGINAL_REL"
  print_command 'proverif[original][COMPONENT]' cpp -P -D COMPONENT "$PROVERIF_ORIGINAL_REL"
  print_command 'proverif[hmac][HMAC_BASELINE]' cpp -P -D HMAC_BASELINE "$PROVERIF_HMAC_REL"
  print_command 'proverif[hmac][HMAC_COMPONENT]' cpp -P -D HMAC_COMPONENT "$PROVERIF_HMAC_REL"
  print_command 'trace[duplicate-fail]' tamarin-prover --derivcheck-timeout=0 --prove=duplicate_batch_fail_exists --output-json=trace.json --output-dot=trace.dot "$FIXED_REPLAY_REL"
  print_command 'trace[distinct-complete]' tamarin-prover --derivcheck-timeout=0 --prove=normal_distinct_batch_complete --output-json=trace.json --output-dot=trace.dot "$FIXED_REPLAY_REL"
  print_command 'trace[distinct-fail-slot1]' tamarin-prover --derivcheck-timeout=0 --prove=normal_distinct_fail_slot1_exists --output-json=trace.json --output-dot=trace.dot "$FIXED_REPLAY_REL"
  print_command 'trace[distinct-fail-slot2]' tamarin-prover --derivcheck-timeout=0 --prove=normal_distinct_fail_slot2_exists --output-json=trace.json --output-dot=trace.dot "$FIXED_REPLAY_REL"
  print_command 'trace[distinct-consumer]' tamarin-prover --derivcheck-timeout=0 --prove=normal_distinct_consumer_complete --output-json=trace.json --output-dot=trace.dot "$FIXED_IMPACT_REL"
} > "$COMMAND_LOG"

{
  echo "repository_path: $ROOT_DIR"
  echo "actual_runner_path: $RUNNER_PATH"
  echo "utc_start: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "git_branch: $GIT_BRANCH"
  echo "git_head: $GIT_HEAD"
  echo "git_tree: $GIT_TREE"
  echo "execution_mode: sequential_per_exact_lemma"
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
  echo
  echo "tamarin-prover --version:"
  tamarin-prover --version
  echo
  echo "maude --version:"
  maude --version
  echo
  echo "proverif version:"
  "${PROVERIF_CMD[@]}" -version 2>&1 || true
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
parse_fixed_replay_status=0
parse_fixed_impact_status=0
tamarin-prover --parse-only "$FIXED_REPLAY_REL" > "$LOG_DIR/parse/fixed-replay.out" 2>&1 || parse_fixed_replay_status=$?
tamarin-prover --parse-only "$FIXED_IMPACT_REL" > "$LOG_DIR/parse/fixed-impact.out" 2>&1 || parse_fixed_impact_status=$?

fixed_replay_status=0; fixed_impact_status=0; original_replay_status=0
hmac_replay_status=0; original_impact_status=0; v6_status=0; v7_status=0
run_tamarin_suite fixed-replay "$FIXED_REPLAY_REL" FIXED_REPLAY_LEMMAS FIXED_REPLAY_EXPECTED || fixed_replay_status=1
run_tamarin_suite fixed-impact "$FIXED_IMPACT_REL" FIXED_IMPACT_LEMMAS FIXED_IMPACT_EXPECTED || fixed_impact_status=1
run_tamarin_suite original-replay "$ORIGINAL_REPLAY_REL" REPLAY_FROZEN ORIGINAL_REPLAY_EXPECTED || original_replay_status=1
run_tamarin_suite hmac-replay "$HMAC_REPLAY_REL" HMAC_REPLAY_LEMMAS HMAC_REPLAY_EXPECTED || hmac_replay_status=1
run_tamarin_suite original-impact "$ORIGINAL_IMPACT_REL" ORIGINAL_IMPACT_LEMMAS ORIGINAL_IMPACT_EXPECTED || original_impact_status=1
run_tamarin_suite v6 "$V6_REL" V6_LEMMAS V6_EXPECTED || v6_status=1
run_tamarin_suite v7 "$V7_REL" V7_LEMMAS V7_EXPECTED || v7_status=1

proverif_status=0
run_proverif_target proverif-original BASELINE "$PROVERIF_ORIGINAL_REL" "$PROVERIF_ORIGINAL_BASELINE_REL" || proverif_status=1
run_proverif_target proverif-original COMPONENT "$PROVERIF_ORIGINAL_REL" "$PROVERIF_ORIGINAL_BASELINE_REL" || proverif_status=1
run_proverif_target proverif-hmac HMAC_BASELINE "$PROVERIF_HMAC_REL" "$PROVERIF_HMAC_BASELINE_REL" || proverif_status=1
run_proverif_target proverif-hmac HMAC_COMPONENT "$PROVERIF_HMAC_REL" "$PROVERIF_HMAC_BASELINE_REL" || proverif_status=1

trace_status=0
run_trace duplicate-fail "$FIXED_REPLAY_REL" duplicate_batch_fail_exists || trace_status=1
run_trace distinct-complete "$FIXED_REPLAY_REL" normal_distinct_batch_complete || trace_status=1
run_trace distinct-fail-slot1 "$FIXED_REPLAY_REL" normal_distinct_fail_slot1_exists || trace_status=1
run_trace distinct-fail-slot2 "$FIXED_REPLAY_REL" normal_distinct_fail_slot2_exists || trace_status=1
run_trace distinct-consumer "$FIXED_IMPACT_REL" normal_distinct_consumer_complete || trace_status=1

POST_RUN_GIT_STATUS="$("${GIT_CMD[@]}" status --porcelain=v1 --untracked-files=all)"
UNEXPECTED_STATUS="$(printf '%s\n' "$POST_RUN_GIT_STATUS" | awk -v prefix="?? $LOG_REL/" 'NF && index($0,prefix) != 1 {print}')"

{
  echo "K-Waay M3 batch-local atomic dedup evidence summary"
  echo "git_head: $GIT_HEAD"
  echo "git_tree: $GIT_TREE"
  echo "parse_fixed_replay_status: $parse_fixed_replay_status"
  echo "parse_fixed_impact_status: $parse_fixed_impact_status"
  echo "fixed_replay_status: $fixed_replay_status"
  echo "fixed_impact_status: $fixed_impact_status"
  echo "original_replay_regression_status: $original_replay_status"
  echo "hmac_replay_regression_status: $hmac_replay_status"
  echo "original_impact_regression_status: $original_impact_status"
  echo "v6_regression_status: $v6_status"
  echo "v7_regression_status: $v7_status"
  echo "proverif_regression_status: $proverif_status"
  echo "formula_comparison_status: $formula_status"
  echo "constructor_comparison_status: $constructor_status"
  echo "consumer_rule_comparison_status: $consumer_rule_status"
  echo "trace_status: $trace_status"
  echo "post_run_unexpected_status_empty: $([[ -z "$UNEXPECTED_STATUS" ]] && echo true || echo false)"
} > "$SUMMARY_LOG"

{
  echo
  echo "utc_end: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  cat "$SUMMARY_LOG"
  echo "post_run_git_status:"
  printf '%s\n' "$POST_RUN_GIT_STATUS"
} >> "$VERSIONS_LOG"

(
  cd "$LOG_DIR"
  find . -type f ! -name 'SHA256SUMS.txt' -printf '%P\0' \
    | LC_ALL=C sort -z \
    | xargs -0 sha256sum
) > "$MANIFEST_LOG"

cat "$SUMMARY_LOG"

final_status=0
for status in \
  "$parse_fixed_replay_status" "$parse_fixed_impact_status" \
  "$fixed_replay_status" "$fixed_impact_status" \
  "$original_replay_status" "$hmac_replay_status" "$original_impact_status" \
  "$v6_status" "$v7_status" "$proverif_status" \
  "$formula_status" "$constructor_status" "$consumer_rule_status" "$trace_status"; do
  [[ "$status" == 0 ]] || final_status=1
done
if [[ -n "$UNEXPECTED_STATUS" ]]; then
  echo "error: unexpected post-run worktree changes" >&2
  printf '%s\n' "$UNEXPECTED_STATUS" >&2
  final_status=1
fi

exit "$final_status"
