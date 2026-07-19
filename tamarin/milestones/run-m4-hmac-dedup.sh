#!/usr/bin/env bash

set -euo pipefail

# Commit A freezes both the target inventory and the evidence-selection policy.
# --static-only performs no proof and creates no log directory.
# --source-run N invokes every required target and writes source-runN.
# --assemble-composite mechanically applies the Run-1-primary policy.

RUNNER_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
RUNNER_DIR="$(dirname "$RUNNER_PATH")"
ROOT_DIR="$(cd "$RUNNER_DIR/../.." && pwd -P)"
RUNNER_REL="tamarin/milestones/run-m4-hmac-dedup.sh"

COMBINED_REPLAY_REL="tamarin/replay/kwaay_replay_hmac_dedup.spthy"
COMBINED_IMPACT_REL="tamarin/impact/kwaay_impact_hmac_dedup.spthy"
COMBINED_REPLAY_README_REL="tamarin/replay/README-hmac-dedup.md"
COMBINED_IMPACT_README_REL="tamarin/impact/README-hmac-dedup.md"
ORIGINAL_REPLAY_REL="tamarin/replay/kwaay_replay_original.spthy"
HMAC_REPLAY_REL="tamarin/replay/kwaay_replay_hmac_only.spthy"
FIXED_REPLAY_REL="tamarin/replay/kwaay_replay_fixed.spthy"
ORIGINAL_IMPACT_REL="tamarin/impact/kwaay_impact_original.spthy"
FIXED_IMPACT_REL="tamarin/impact/kwaay_impact_fixed.spthy"
V6_REL="tamarin/kwaay_splitkem_batch_dynamic_v6.spthy"
V7_REL="tamarin/kwaay_splitkem_batch_dynamic_v7.spthy"
PROVERIF_ORIGINAL_REL="proverif/kwaay_core_final.cpp.pv"
PROVERIF_HMAC_REL="proverif/variants/hmac-confirmation/kwaay_core_hmac_confirmation.cpp.pv"
PROVERIF_ORIGINAL_BASELINE_REL="logs/final/proverif/summary.txt"
PROVERIF_HMAC_BASELINE_REL="logs/variants/hmac-confirmation/proverif/summary.txt"
LOG_REL="logs/tamarin-m4-hmac-dedup"
LOG_DIR="$ROOT_DIR/$LOG_REL"
PROOF_TIMEOUT_SECONDS=300

REPLAY_HMAC=(
  normal_confirmed_single_accept normal_confirmed_batch_complete
  confirmed_receiver_accept_has_sender confirmed_message_unique_send
  one_confirmed_send_two_accepts_exists confirmed_message_accepted_at_most_once
  injective_confirmed_receiver_accept slot_indices_distinct
  process_requires_slot_added process_requires_seal
  complete_requires_all_slots_processed no_add_after_seal no_accept_after_close
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use receiver_state_single_batch receiver_state_single_batch_end
)

REPLAY_M3=(
  duplicate_batch_fail_exists duplicate_detected_before_any_accept
  duplicate_batch_has_no_accept process_requires_dedup_pass
  dedup_pass_messages_distinct dedup_decision_single_use dedup_outcomes_exclusive
  normal_distinct_batch_complete normal_distinct_fail_slot1_exists
  normal_distinct_fail_slot2_exists batch_fail_complete_exclusive
  state_consumed_on_duplicate_fail
)

REPLAY_COMBINED=(
  confirmed_base_message_accepted_at_most_once
  duplicate_same_base_different_tag_fail_exists
  confirmed_accept_requires_valid_tag confirmed_accept_requires_hmac_validated
  hmac_failure_slot1_exists hmac_failure_slot2_after_prior_accept_replay_exists
  hmac_failed_slot_has_no_accept
  normal_two_distinct_valid_confirmed_accepts_complete
)

COMBINED_REPLAY_TARGETS=("${REPLAY_HMAC[@]}" "${REPLAY_M3[@]}" "${REPLAY_COMBINED[@]}")

IMPACT_COMPOSITION=(
  accept_output_has_same_time_confirmed_accept confirmed_receiver_accept_has_output
  confirmed_receiver_accept_has_unique_output accept_id_unique install_has_prior_accept
  install_session_has_interface_origin install_from_accept_has_session
  install_event_has_single_source install_handle_unique
  accept_output_installed_at_most_once distinct_accept_sources_have_distinct_handles
  install_requires_batch_complete consumer_complete_requires_all_outputs_installed
  consumer_complete_single_use no_install_after_consumer_close
  normal_one_confirmed_accept_one_install
  legacy_same_confirmed_message_consumer_complete_exists
  one_confirmed_send_two_accepts_two_installs_exists
  unique_install_within_completed_consumer
)

IMPACT_ONLY=(
  duplicate_batch_has_no_accept_output duplicate_batch_has_no_install
  normal_two_distinct_valid_confirmed_outputs_consumer_complete
  no_consumer_after_failed_batch hmac_failure_slot2_after_prior_accept_exists
)

COMBINED_IMPACT_TARGETS=("${COMBINED_REPLAY_TARGETS[@]}" "${IMPACT_COMPOSITION[@]}" "${IMPACT_ONLY[@]}")

ORIGINAL_REPLAY_TARGETS=(
  normal_single_accept normal_batch_complete one_send_two_accepts_exists
  same_message_accepted_at_most_once full_message_unique_send
  receiver_accept_has_sender injective_receiver_accept slot_indices_distinct
  process_requires_slot_added process_requires_seal
  complete_requires_all_slots_processed no_add_after_seal no_accept_after_close
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use receiver_state_single_batch receiver_state_single_batch_end
)

HMAC_REPLAY_TARGETS=("${REPLAY_HMAC[@]}")

ORIGINAL_IMPACT_COMPOSITION=(
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

FIXED_REPLAY_M3=(
  duplicate_batch_fail_exists duplicate_detected_before_any_accept
  duplicate_batch_has_no_accept process_requires_dedup_pass
  dedup_pass_messages_distinct dedup_decision_single_use dedup_outcomes_exclusive
  normal_distinct_batch_complete normal_distinct_fail_slot1_exists
  normal_distinct_fail_slot2_exists batch_fail_complete_exclusive
  state_consumed_on_duplicate_fail
)

FIXED_IMPACT_M3=(
  duplicate_batch_fail_exists duplicate_detected_before_any_accept
  duplicate_batch_has_no_accept duplicate_batch_has_no_accept_output
  duplicate_batch_has_no_install process_requires_dedup_pass
  dedup_pass_messages_distinct dedup_decision_single_use dedup_outcomes_exclusive
  normal_distinct_batch_complete normal_distinct_consumer_complete
  normal_distinct_fail_slot1_exists normal_distinct_fail_slot2_exists
  batch_fail_complete_exclusive state_consumed_on_duplicate_fail
  no_consumer_after_failed_batch
)

ORIGINAL_IMPACT_TARGETS=("${ORIGINAL_IMPACT_COMPOSITION[@]}" "${ORIGINAL_REPLAY_TARGETS[@]}")
FIXED_REPLAY_TARGETS=("${ORIGINAL_REPLAY_TARGETS[@]}" "${FIXED_REPLAY_M3[@]}")
FIXED_IMPACT_TARGETS=("${ORIGINAL_IMPACT_COMPOSITION[@]}" "${ORIGINAL_REPLAY_TARGETS[@]}" "${FIXED_IMPACT_M3[@]}")

V6_TARGETS=(
  executable_add_slot executable_seal_batch executable_process_slot
  executable_batch_complete executable_batch_fail process_requires_slot_added
  process_requires_seal complete_requires_seal fail_requires_seal
  batch_complete_consumes_state batch_fail_consumes_state
  batch_end_token_single_use batch_fail_complete_exclusive
  slot_origin_without_early_compromise slot_key_known_requires_exception
  partnered_slot_key_not_attacker_known_without_early_compromise
)

V7_TARGETS=(
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

PROVERIF_ORIGINAL_TARGETS=(BASELINE COMPONENT)
PROVERIF_HMAC_TARGETS=(HMAC_BASELINE HMAC_COMPONENT HMAC_LEAK_SIGSK_A)

declare -A EXPECT_COMBINED_REPLAY=() EXPECT_COMBINED_IMPACT=()
declare -A EXPECT_ORIGINAL_REPLAY=() EXPECT_HMAC_REPLAY=()
declare -A EXPECT_ORIGINAL_IMPACT=() EXPECT_FIXED_REPLAY=() EXPECT_FIXED_IMPACT=()
declare -A EXPECT_V6=() EXPECT_V7=()

set_all_expected() {
  local array_name="$1" map_name="$2" value="$3" item
  local -n arr="$array_name" map="$map_name"
  for item in "${arr[@]}"; do map["$item"]="$value"; done
}

set_all_expected COMBINED_REPLAY_TARGETS EXPECT_COMBINED_REPLAY verified
EXPECT_COMBINED_REPLAY[one_confirmed_send_two_accepts_exists]=falsified
set_all_expected COMBINED_IMPACT_TARGETS EXPECT_COMBINED_IMPACT verified
EXPECT_COMBINED_IMPACT[one_confirmed_send_two_accepts_exists]=falsified
EXPECT_COMBINED_IMPACT[legacy_same_confirmed_message_consumer_complete_exists]=falsified
EXPECT_COMBINED_IMPACT[one_confirmed_send_two_accepts_two_installs_exists]=falsified
set_all_expected ORIGINAL_REPLAY_TARGETS EXPECT_ORIGINAL_REPLAY verified
EXPECT_ORIGINAL_REPLAY[same_message_accepted_at_most_once]=falsified
EXPECT_ORIGINAL_REPLAY[injective_receiver_accept]=falsified
set_all_expected HMAC_REPLAY_TARGETS EXPECT_HMAC_REPLAY verified
EXPECT_HMAC_REPLAY[confirmed_message_accepted_at_most_once]=falsified
EXPECT_HMAC_REPLAY[injective_confirmed_receiver_accept]=falsified
set_all_expected ORIGINAL_IMPACT_TARGETS EXPECT_ORIGINAL_IMPACT verified
EXPECT_ORIGINAL_IMPACT[unique_install_within_completed_consumer]=falsified
EXPECT_ORIGINAL_IMPACT[same_message_accepted_at_most_once]=falsified
EXPECT_ORIGINAL_IMPACT[injective_receiver_accept]=falsified
set_all_expected FIXED_REPLAY_TARGETS EXPECT_FIXED_REPLAY verified
EXPECT_FIXED_REPLAY[one_send_two_accepts_exists]=falsified
set_all_expected FIXED_IMPACT_TARGETS EXPECT_FIXED_IMPACT verified
EXPECT_FIXED_IMPACT[one_send_two_accepts_exists]=falsified
EXPECT_FIXED_IMPACT[normal_consumer_complete]=falsified
EXPECT_FIXED_IMPACT[one_send_two_accepts_two_installs_exists]=falsified
set_all_expected V6_TARGETS EXPECT_V6 verified
set_all_expected V7_TARGETS EXPECT_V7 verified

FROZEN_PATHS=(
  "$ORIGINAL_REPLAY_REL" "$HMAC_REPLAY_REL" "$FIXED_REPLAY_REL"
  "$ORIGINAL_IMPACT_REL" "$FIXED_IMPACT_REL" "$V6_REL" "$V7_REL"
  "$PROVERIF_ORIGINAL_REL" "$PROVERIF_HMAC_REL"
  "$PROVERIF_ORIGINAL_BASELINE_REL" "$PROVERIF_HMAC_BASELINE_REL"
)

declare -A FROZEN_BLOB=() FROZEN_SHA256=()
FROZEN_BLOB["$ORIGINAL_REPLAY_REL"]="e3699da2f827a683ded2feaaa7db2d51ad74c023"
FROZEN_SHA256["$ORIGINAL_REPLAY_REL"]="064ec603bdfac917246a12762774701bc624c40ccb11eb6a88adf94befb4322e"
FROZEN_BLOB["$HMAC_REPLAY_REL"]="589e8693f23d76fcf3977d6ca3784a2f670d5d8d"
FROZEN_SHA256["$HMAC_REPLAY_REL"]="d46ead8564b8cc8410f9f3a655c72be440e5fce3f2455022e0b00155508873f6"
FROZEN_BLOB["$FIXED_REPLAY_REL"]="493568857492e9c17b896dfb2ab3692f7b48d365"
FROZEN_SHA256["$FIXED_REPLAY_REL"]="7d5ebdca2b5f71856d4e94a18ddce17212bd25c7dd869f3495a123ae521452b3"
FROZEN_BLOB["$ORIGINAL_IMPACT_REL"]="c5cdc0d7233f3a415839b8f289182c0986d911a8"
FROZEN_SHA256["$ORIGINAL_IMPACT_REL"]="0c20e36137c27bd138101a91ef5ce1e16109fccf696f942eb98c3d855a11fa41"
FROZEN_BLOB["$FIXED_IMPACT_REL"]="3a707c022594ce84f23c2f39623715fe3c3f47e2"
FROZEN_SHA256["$FIXED_IMPACT_REL"]="0c46643fb278598d45b91dc2ce4a963ab1a7f3336581a5afe599cc888b9bd808"
FROZEN_BLOB["$V6_REL"]="cc7d7d962bbe1bc8d8e09354ca8fdf911be865f9"
FROZEN_SHA256["$V6_REL"]="7733815c2a176d9bd0ca411b6ff7d966e0eaba9f9e377523af0e614697a5e302"
FROZEN_BLOB["$V7_REL"]="7c8c73eb795ee5fd8196654af2a6ecf04a73b380"
FROZEN_SHA256["$V7_REL"]="7dd91deac3e16fbb600b1dd646e6c783aa56ce779b9097216bba0814e7b37a47"
FROZEN_BLOB["$PROVERIF_ORIGINAL_REL"]="f8fded3f616d7b6e203933921922ef049437e36b"
FROZEN_SHA256["$PROVERIF_ORIGINAL_REL"]="b28b8145992d96f190cc478608b7e36669f0040a06319a63f2d69969347de867"
FROZEN_BLOB["$PROVERIF_HMAC_REL"]="69d27acf560552293b486f5667b6be50e331fa93"
FROZEN_SHA256["$PROVERIF_HMAC_REL"]="940fdb4a0449a0d35a70f488d1c68f6e79884cf5651419c96b1d65aa295b04bd"
FROZEN_BLOB["$PROVERIF_ORIGINAL_BASELINE_REL"]="ff24b5e33537be899d1f25c8a825e02e8054cf2f"
FROZEN_SHA256["$PROVERIF_ORIGINAL_BASELINE_REL"]="b3a59616ae0d9a3eeb81d878515fdd79e29cbf4951fcf6029e2eb6944bd6075e"
FROZEN_BLOB["$PROVERIF_HMAC_BASELINE_REL"]="41162bc55aeb077d65a0c259a1c96e050a718325"
FROZEN_SHA256["$PROVERIF_HMAC_BASELINE_REL"]="6de331e25170c36f893ceb78888fd12dbefe3f47b952bda98dfe40d51aa2c503"

git_cmd() { git -c "safe.directory=$ROOT_DIR" -C "$ROOT_DIR" "$@"; }

extract_lemmas() { sed -n 's/^lemma[[:space:]]\+\([A-Za-z0-9_]\+\):.*/\1/p' "$1"; }

check_inventory() {
  local file="$1" array_name="$2" label="$3" tmp_actual tmp_expected
  local -n arr="$array_name"
  tmp_actual="$(mktemp)"; tmp_expected="$(mktemp)"
  extract_lemmas "$file" | sort > "$tmp_actual"
  printf '%s\n' "${arr[@]}" | sort > "$tmp_expected"
  if [[ "$(wc -l < "$tmp_actual")" -ne "$(sort -u "$tmp_actual" | wc -l)" ]]; then
    echo "error: duplicate lemma name in $label" >&2; return 1
  fi
  if ! diff -u "$tmp_expected" "$tmp_actual"; then
    echo "error: theory/runner target mismatch for $label" >&2; return 1
  fi
  rm -f "$tmp_actual" "$tmp_expected"
  printf '%s_count=%s\n' "$label" "${#arr[@]}"
}

extract_block() {
  local kind="$1" name="$2" file="$3"
  awk -v head="$kind $name:" '
    {sub(/\r$/,"")}
    $0 == head {inside=1}
    inside && $0 != head && ($0 ~ /^rule [A-Za-z0-9_]+:/ || $0 ~ /^lemma [A-Za-z0-9_]+:/ || $0 ~ /^\/\*/ || $0 ~ /^end$/) {exit}
    inside {print}
  ' "$file"
}

normalize_text() {
  sed -E 's@/\*([^*]|\*+[^*/])*\*/@@g; s@//.*$@@' | tr -d '[:space:]'
}

compare_rule_normalized() {
  local name="$1" source="$2" target="$3" projection="${4:-none}" a b
  a="$(mktemp)"; b="$(mktemp)"
  extract_block rule "$name" "$source" | normalize_text > "$a"
  extract_block rule "$name" "$target" | normalize_text > "$b"
  if [[ "$projection" == "drop-tags" ]]; then
    sed -E -i 's/<m([12]?),tag[12]?>/m\1/g; s/,tag[12]?//g' "$b"
  fi
  if ! cmp -s "$a" "$b"; then
    diff -u "$a" "$b" >&2 || true
    rm -f "$a" "$b"
    echo "error: normalized rule mismatch: $name" >&2
    return 1
  fi
  rm -f "$a" "$b"
}

compare_formula_exact() {
  local name="$1" source="$2" target="$3" a b
  a="$(mktemp)"; b="$(mktemp)"
  extract_block lemma "$name" "$source" | normalize_text > "$a"
  extract_block lemma "$name" "$target" | normalize_text > "$b"
  if ! cmp -s "$a" "$b"; then
    rm -f "$a" "$b"
    echo "error: formula mismatch: $name" >&2
    return 1
  fi
  rm -f "$a" "$b"
}

static_checks() {
  local failures=0 functions_a functions_b rule
  for path in "$COMBINED_REPLAY_REL" "$COMBINED_IMPACT_REL" \
              "$COMBINED_REPLAY_README_REL" "$COMBINED_IMPACT_README_REL"; do
    [[ -f "$ROOT_DIR/$path" ]] || { echo "error: missing $path" >&2; failures=1; }
  done
  check_inventory "$ROOT_DIR/$COMBINED_REPLAY_REL" COMBINED_REPLAY_TARGETS combined_replay || failures=1
  check_inventory "$ROOT_DIR/$COMBINED_IMPACT_REL" COMBINED_IMPACT_TARGETS combined_impact || failures=1

  if grep -P -n '(^|[^A-Za-z0-9_])(SenderSession|ReceiverAccept)\(' \
      "$ROOT_DIR/$COMBINED_REPLAY_REL" "$ROOT_DIR/$COMBINED_IMPACT_REL"; then
    echo "error: forbidden alias event token" >&2; failures=1
  fi
  for file in "$ROOT_DIR/$COMBINED_REPLAY_REL" "$ROOT_DIR/$COMBINED_IMPACT_REL"; do
    [[ "$(awk '/^lemma /{exit} /Neq\(/{n++} END{print n+0}' "$file")" -eq 2 ]] || {
      echo "error: Neq must occur before lemmas only in restriction and PassDistinctBatch" >&2; failures=1; }
    grep -q 'In(<\$A,\$B,<m,tag>>)' "$file" || failures=1
    grep -q 'ConfirmedSend(\$A,\$B,m,sid,k,tag)' "$file" || failures=1
    grep -q 'ConfirmedReceiverAccept(\$B,\$A,bid,idx,rst,m,sid,k,expected)' "$file" || failures=1
  done

  functions_a="$(awk '{sub(/\r$/,"")} /^functions:/{p=1} p{print} p && /^$/{exit}' "$ROOT_DIR/$HMAC_REPLAY_REL" | normalize_text)"
  functions_b="$(awk '{sub(/\r$/,"")} /^functions:/{p=1} p{print} p && /^$/{exit}' "$ROOT_DIR/$COMBINED_REPLAY_REL" | normalize_text)"
  [[ "$functions_a" == "$functions_b" ]] || { echo "error: HMAC functions block mismatch" >&2; failures=1; }
  compare_rule_normalized SenderCreatesConfirmedMessage "$ROOT_DIR/$HMAC_REPLAY_REL" "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  compare_formula_exact confirmed_receiver_accept_has_sender "$ROOT_DIR/$HMAC_REPLAY_REL" "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  compare_formula_exact confirmed_message_unique_send "$ROOT_DIR/$HMAC_REPLAY_REL" "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  for rule in ProcessSlot1 ProcessSlot2; do
    block="$(extract_block rule "$rule" "$ROOT_DIR/$COMBINED_REPLAY_REL")"
    grep -q 'expected = hmac(confirm_key(k),sid)' <<<"$block" || failures=1
    grep -q '!HonestSession(\$A,\$B,rst,m,sid,k)' <<<"$block" || failures=1
    grep -q 'HmacValidated(\$B,\$A,bid,idx,rst,m,sid,k,expected)' <<<"$block" || failures=1
    grep -q 'ConfirmedReceiverAccept(\$B,\$A,bid,idx,rst,m,sid,k,expected)' <<<"$block" || failures=1
  done

  for rule in InstallAcceptedOutputFirst InstallAcceptedOutputSecond CompleteConsumer; do
    compare_rule_normalized "$rule" "$ROOT_DIR/$FIXED_IMPACT_REL" "$ROOT_DIR/$COMBINED_IMPACT_REL" || failures=1
  done
  for rule in SealBatch RejectDuplicateBatch PassDistinctBatch FailSlot1 FailSlot2; do
    compare_rule_normalized "$rule" "$ROOT_DIR/$FIXED_REPLAY_REL" "$ROOT_DIR/$COMBINED_REPLAY_REL" drop-tags || failures=1
  done
  for formula in dedup_pass_messages_distinct dedup_decision_single_use dedup_outcomes_exclusive state_consumed_on_duplicate_fail; do
    compare_formula_exact "$formula" "$ROOT_DIR/$FIXED_REPLAY_REL" "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  done
  for event in DedupPending DedupDecisionToken DuplicateDetected DedupPassed UseDedupDecisionToken UseBatchEndToken; do
    grep -q "$event(" "$ROOT_DIR/$COMBINED_REPLAY_REL" || { echo "error: missing $event" >&2; failures=1; }
  done
  grep -q 'HmacValidationFailed(' "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  grep -q '#hf < #bf' "$ROOT_DIR/$COMBINED_REPLAY_REL" || failures=1
  verify_frozen_inputs || failures=1

  if [[ "$failures" -ne 0 ]]; then return 1; fi
  echo "consumer_rules=3/3 MATCH"
  echo "hmac_functions=MATCH"
  echo "hmac_sender_rule=MATCH"
  echo "hmac_matching_formulas=2/2 MATCH"
  echo "m3_dedup_structure=MATCH_WITH_APPROVED_TAG_PROJECTION"
  echo "alias_tokens=ABSENT"
  echo "frozen_blobs_and_sha256=MATCH"
  echo "static_checks=PASS"
}

verify_frozen_inputs() {
  local path blob sha
  for path in "${FROZEN_PATHS[@]}"; do
    blob="$(git_cmd rev-parse "HEAD:$path")"
    sha="$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    [[ "$blob" == "${FROZEN_BLOB[$path]}" ]] || { echo "error: frozen blob drift: $path" >&2; return 1; }
    [[ "$sha" == "${FROZEN_SHA256[$path]}" ]] || { echo "error: frozen SHA drift: $path" >&2; return 1; }
  done
}

parse_tamarin_result() {
  local target="$1" raw="$2" line
  if grep -q '<<loop>>' "$raw"; then printf 'nonterminal'; return; fi
  line="$(grep -E "^[[:space:]]*$target \((all-traces|exists-trace)\): (verified|falsified)" "$raw" | tail -n1 || true)"
  if [[ "$line" == *": verified"* ]]; then printf 'verified'
  elif [[ "$line" == *": falsified"* ]]; then printf 'falsified'
  else printf 'nonterminal'; fi
}

run_tamarin_suite() {
  local out="$1" suite="$2" model="$3" array_name="$4" map_name="$5"
  local -n targets="$array_name" expected_map="$map_name"
  local target raw status exit_code loop
  mkdir -p "$out/proofs/$suite"
  for target in "${targets[@]}"; do
    raw="$out/proofs/$suite/$target.out"; exit_code=0
    printf 'tamarin-prover --derivcheck-timeout=0 --prove=%q %q\n' "$target" "$model" >> "$out/commands.txt"
    timeout "$PROOF_TIMEOUT_SECONDS" tamarin-prover --derivcheck-timeout=0 "--prove=$target" "$model" > "$raw" 2>&1 || exit_code=$?
    status="$(parse_tamarin_result "$target" "$raw")"
    loop=false; grep -q '<<loop>>' "$raw" && loop=true
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$status" \
      "${expected_map[$target]}" "$exit_code" "$loop" "proofs/$suite/$target.out" >> "$out/aggregate.tsv"
  done
}

extract_pv_results() {
  local summary="$1" target="$2"
  awk -v target="$target" '
    $0 == "TARGET: " target {inside=1; next}
    inside && /^TARGET: / {exit}
    inside && /^RESULT / {sub(/\r$/,""); print}
  ' "$summary"
}

run_proverif_target() {
  local out="$1" suite="$2" target="$3" model="$4" baseline="$5"
  local generated raw actual expected exit_code=0 status=nonterminal
  mkdir -p "$out/proverif/$suite/generated" "$out/proverif/$suite/out"
  generated="$out/proverif/$suite/generated/$target.pv"
  raw="$out/proverif/$suite/out/$target.out"
  printf 'cpp -P -D %q %q > %q\n' "$target" "$model" "$generated" >> "$out/commands.txt"
  cpp -P -D "$target" "$model" > "$generated"
  printf 'proverif %q\n' "$generated" >> "$out/commands.txt"
  timeout "$PROOF_TIMEOUT_SECONDS" proverif "$generated" > "$raw" 2>&1 || exit_code=$?
  actual="$(mktemp)"; expected="$(mktemp)"
  grep '^RESULT ' "$raw" | sed 's/\r$//' > "$actual" || true
  extract_pv_results "$baseline" "$target" > "$expected"
  if [[ "$exit_code" -eq 0 ]] && cmp -s "$actual" "$expected"; then status=MATCH; fi
  rm -f "$actual" "$expected"
  printf '%s\t%s\t%s\tMATCH\t%s\tfalse\t%s\n' "$suite" "$target" "$status" "$exit_code" \
    "proverif/$suite/out/$target.out" >> "$out/aggregate.tsv"
}

write_provenance() {
  local out="$1"
  {
    echo "git_head=$(git_cmd rev-parse HEAD)"
    echo "git_tree=$(git_cmd show -s --format=%T HEAD)"
    echo "git_branch=$(git_cmd branch --show-current)"
    echo "runner_blob=$(git_cmd rev-parse HEAD:$RUNNER_REL)"
    echo "runner_sha256=$(sha256sum "$ROOT_DIR/$RUNNER_REL" | awk '{print $1}')"
    echo "combined_replay_blob=$(git_cmd rev-parse HEAD:$COMBINED_REPLAY_REL)"
    echo "combined_replay_sha256=$(sha256sum "$ROOT_DIR/$COMBINED_REPLAY_REL" | awk '{print $1}')"
    echo "combined_impact_blob=$(git_cmd rev-parse HEAD:$COMBINED_IMPACT_REL)"
    echo "combined_impact_sha256=$(sha256sum "$ROOT_DIR/$COMBINED_IMPACT_REL" | awk '{print $1}')"
    echo "proof_timeout_seconds=$PROOF_TIMEOUT_SECONDS"
    echo "command=$RUNNER_REL --source-run"
    tamarin-prover --version 2>&1 | sed 's/^/tamarin=/'
    maude --version 2>&1 | head -n3 | sed 's/^/maude=/'
    proverif -version 2>&1 | sed 's/^/proverif=/' || true
  } > "$out/provenance.txt"
}

make_manifest() {
  local out="$1"
  (cd "$out" && find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS.txt)
  (cd "$out" && sha256sum -c SHA256SUMS.txt)
}

write_formula_digests() {
  local out="$1" suite="$2" model="$3" array_name="$4" target digest
  local -n targets="$array_name"
  for target in "${targets[@]}"; do
    digest="$(extract_block lemma "$target" "$model" | normalize_text | sha256sum | awk '{print $1}')"
    printf '%s\t%s\t%s\n' "$suite" "$target" "$digest" >> "$out/formula-bodies.tsv"
  done
}

write_frozen_input_table() {
  local out="$1" path blob sha
  printf 'path\tblob\tsha256\n' > "$out/frozen-inputs.tsv"
  for path in "${FROZEN_PATHS[@]}"; do
    blob="$(git_cmd rev-parse "HEAD:$path")"
    sha="$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    printf '%s\t%s\t%s\n' "$path" "$blob" "$sha" >> "$out/frozen-inputs.tsv"
  done
}

terminal_status() { [[ "$1" == verified || "$1" == falsified || "$1" == MATCH ]]; }

source_run() {
  local n="$1" out="$LOG_DIR/source-run$n" status
  [[ "$n" == 1 || "$n" == 2 ]] || { echo "error: source run must be 1 or 2" >&2; exit 2; }
  static_checks; verify_frozen_inputs
  [[ -z "$(git_cmd status --porcelain=v1 --untracked-files=all -- . ':!logs/tamarin-m4-hmac-dedup')" ]] || {
    echo "error: tracked/source state is not clean" >&2; exit 2; }
  [[ ! -e "$out" ]] || { echo "error: source run exists: $out" >&2; exit 2; }
  if [[ "$n" == 2 ]]; then
    [[ -f "$LOG_DIR/source-run1/aggregate.tsv" ]] || { echo "error: Run 1 is required" >&2; exit 2; }
    if awk -F '\t' 'NR>1 && $3 != $4 {bad=1} END{exit bad}' "$LOG_DIR/source-run1/aggregate.tsv" \
       && awk -F '\t' 'NR>1 && $3 == "nonterminal" {bad=1} END{exit bad}' "$LOG_DIR/source-run1/aggregate.tsv"; then
      echo "error: Run 1 is complete and matches expected; Run 2 is forbidden" >&2; exit 2
    fi
  fi
  mkdir -p "$out/parse"
  printf 'suite\ttarget\tactual_status\texpected_status\texit_status\tloop\traw_output\n' > "$out/aggregate.tsv"
  printf 'suite\ttarget\tformula_body_sha256\n' > "$out/formula-bodies.tsv"
  : > "$out/commands.txt"
  write_provenance "$out"
  write_frozen_input_table "$out"
  static_checks > "$out/static-comparison.txt"
  write_formula_digests "$out" combined-replay "$ROOT_DIR/$COMBINED_REPLAY_REL" COMBINED_REPLAY_TARGETS
  write_formula_digests "$out" combined-impact "$ROOT_DIR/$COMBINED_IMPACT_REL" COMBINED_IMPACT_TARGETS
  write_formula_digests "$out" original-replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" ORIGINAL_REPLAY_TARGETS
  write_formula_digests "$out" hmac-replay "$ROOT_DIR/$HMAC_REPLAY_REL" HMAC_REPLAY_TARGETS
  write_formula_digests "$out" original-impact "$ROOT_DIR/$ORIGINAL_IMPACT_REL" ORIGINAL_IMPACT_TARGETS
  write_formula_digests "$out" fixed-replay "$ROOT_DIR/$FIXED_REPLAY_REL" FIXED_REPLAY_TARGETS
  write_formula_digests "$out" fixed-impact "$ROOT_DIR/$FIXED_IMPACT_REL" FIXED_IMPACT_TARGETS
  write_formula_digests "$out" v6 "$ROOT_DIR/$V6_REL" V6_TARGETS
  write_formula_digests "$out" v7 "$ROOT_DIR/$V7_REL" V7_TARGETS
  printf 'tamarin-prover --parse-only %q\n' "$ROOT_DIR/$COMBINED_REPLAY_REL" >> "$out/commands.txt"
  tamarin-prover --parse-only "$ROOT_DIR/$COMBINED_REPLAY_REL" > "$out/parse/combined-replay.out" 2>&1
  printf 'tamarin-prover --parse-only %q\n' "$ROOT_DIR/$COMBINED_IMPACT_REL" >> "$out/commands.txt"
  tamarin-prover --parse-only "$ROOT_DIR/$COMBINED_IMPACT_REL" > "$out/parse/combined-impact.out" 2>&1
  run_tamarin_suite "$out" combined-replay "$ROOT_DIR/$COMBINED_REPLAY_REL" COMBINED_REPLAY_TARGETS EXPECT_COMBINED_REPLAY
  run_tamarin_suite "$out" combined-impact "$ROOT_DIR/$COMBINED_IMPACT_REL" COMBINED_IMPACT_TARGETS EXPECT_COMBINED_IMPACT
  run_tamarin_suite "$out" original-replay "$ROOT_DIR/$ORIGINAL_REPLAY_REL" ORIGINAL_REPLAY_TARGETS EXPECT_ORIGINAL_REPLAY
  run_tamarin_suite "$out" hmac-replay "$ROOT_DIR/$HMAC_REPLAY_REL" HMAC_REPLAY_TARGETS EXPECT_HMAC_REPLAY
  run_tamarin_suite "$out" original-impact "$ROOT_DIR/$ORIGINAL_IMPACT_REL" ORIGINAL_IMPACT_TARGETS EXPECT_ORIGINAL_IMPACT
  run_tamarin_suite "$out" fixed-replay "$ROOT_DIR/$FIXED_REPLAY_REL" FIXED_REPLAY_TARGETS EXPECT_FIXED_REPLAY
  run_tamarin_suite "$out" fixed-impact "$ROOT_DIR/$FIXED_IMPACT_REL" FIXED_IMPACT_TARGETS EXPECT_FIXED_IMPACT
  run_tamarin_suite "$out" v6 "$ROOT_DIR/$V6_REL" V6_TARGETS EXPECT_V6
  run_tamarin_suite "$out" v7 "$ROOT_DIR/$V7_REL" V7_TARGETS EXPECT_V7
  for status in "${PROVERIF_ORIGINAL_TARGETS[@]}"; do
    run_proverif_target "$out" proverif-original "$status" "$ROOT_DIR/$PROVERIF_ORIGINAL_REL" "$ROOT_DIR/$PROVERIF_ORIGINAL_BASELINE_REL"
  done
  for status in "${PROVERIF_HMAC_TARGETS[@]}"; do
    run_proverif_target "$out" proverif-hmac "$status" "$ROOT_DIR/$PROVERIF_HMAC_REL" "$ROOT_DIR/$PROVERIF_HMAC_BASELINE_REL"
  done
  awk -F '\t' 'NR>1 {n++; if($3=="verified"||$3=="falsified"||$3=="MATCH") t++; if($3!=$4)m++}
    END{printf "invoked=%d\nterminal=%d\nmismatch=%d\n",n,t,m}' "$out/aggregate.tsv" > "$out/summary.txt"
  make_manifest "$out"
  echo "source_run$n=COMPLETE_INVOCATION"
}

assemble_composite() {
  local run1="$LOG_DIR/source-run1" run2="$LOG_DIR/source-run2" selection="$LOG_DIR/composite-selection.tsv"
  local vector="$LOG_DIR/composite-result-vector.tsv" unresolved=0 mismatch=0 conflicts=0
  [[ -f "$run1/aggregate.tsv" ]] || { echo "error: missing Run 1" >&2; exit 2; }
  if [[ -d "$run2" ]]; then
    cmp -s "$run1/provenance.txt" "$run2/provenance.txt" || { echo "error: provenance conflict" >&2; exit 1; }
  fi
  printf 'suite\ttarget\texpected\trun1\trun2\tselected_run\tselected_status\treason\n' > "$selection"
  printf 'suite\ttarget\tactual_status\texpected_status\tselected_run\tmatch\n' > "$vector"
  while IFS=$'\t' read -r suite target r1 expected exit1 loop1 raw1; do
    [[ "$suite" == suite ]] && continue
    local r2=missing selected=none chosen=nonterminal reason="Run 1 nonterminal and no legal fallback"
    if [[ -f "$run2/aggregate.tsv" ]]; then
      r2="$(awk -F '\t' -v s="$suite" -v t="$target" '$1==s&&$2==t{print $3}' "$run2/aggregate.tsv")"
      [[ -n "$r2" ]] || r2=missing
    fi
    if terminal_status "$r1"; then
      selected=run1; chosen="$r1"; reason="Run 1 primary terminal"
      if terminal_status "$r2" && [[ "$r1" != "$r2" ]]; then conflicts=$((conflicts+1)); fi
    elif terminal_status "$r2"; then
      selected=run2; chosen="$r2"; reason="Run 1 nonterminal; legal Run 2 terminal fallback"
    else
      unresolved=$((unresolved+1))
    fi
    [[ "$chosen" == "$expected" ]] || mismatch=$((mismatch+1))
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$expected" "$r1" "$r2" "$selected" "$chosen" "$reason" >> "$selection"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$chosen" "$expected" "$selected" "$([[ "$chosen" == "$expected" ]] && echo MATCH || echo MISMATCH)" >> "$vector"
  done < "$run1/aggregate.tsv"
  {
    echo "classification=transparent composite; Run 1 primary"
    echo "terminal_conflicts=$conflicts"
    echo "unresolved=$unresolved"
    echo "mismatches=$mismatch"
  } > "$LOG_DIR/composite-summary.txt"
  [[ "$conflicts" -eq 0 && "$unresolved" -eq 0 && "$mismatch" -eq 0 ]] || exit 1
  (cd "$LOG_DIR" && find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS.txt)
  echo "composite=PASS"
}

usage() {
  echo "usage: $RUNNER_REL --static-only | --source-run 1|2 | --assemble-composite" >&2
  exit 2
}

case "${1:-}" in
  --static-only)
    [[ $# -eq 1 ]] || usage
    static_checks
    ;;
  --source-run)
    [[ $# -eq 2 ]] || usage
    source_run "$2"
    ;;
  --assemble-composite)
    [[ $# -eq 1 ]] || usage
    assemble_composite
    ;;
  *) usage ;;
esac
