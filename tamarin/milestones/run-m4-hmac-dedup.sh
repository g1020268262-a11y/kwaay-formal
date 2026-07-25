#!/usr/bin/env bash

set -euo pipefail

# Commit A freezes both the target inventory and the evidence-selection policy.
# --static-only performs no proof and creates no log directory.
# --source-run N invokes every required target and writes source-runN.
# --assemble-composite mechanically applies the Run-1-primary policy.
# --self-test exercises validators with synthetic fixtures and never invokes a prover.
#
# Tamarin proof targets run in a per-target user-systemd cgroup with
# MemoryMax=${TAMARIN_MEMORY_MAX_MB}M and MemorySwapMax=0.  The default 6144 MB
# is deliberately below the previously observed WSL-wide OOM point, so one
# pathological target is recorded as nonterminal instead of exhausting the whole
# WSL session.

if [[ -n "${KWAAY_REPO_ROOT+x}" ]]; then
  echo "error: KWAAY_REPO_ROOT is not accepted; the runner derives the repository from its own path" >&2
  exit 2
fi

for bootstrap_command in readlink dirname; do
  command -v "$bootstrap_command" >/dev/null 2>&1 || {
    echo "error: required bootstrap command not found: $bootstrap_command" >&2
    exit 2
  }
done

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
DEFAULT_TAMARIN_MEMORY_MAX_MB=6144
TAMARIN_MEMORY_MAX_MB="${KWAAY_TAMARIN_MEMORY_MAX_MB:-$DEFAULT_TAMARIN_MEMORY_MAX_MB}"
SOURCE_PROGRESS_CURRENT=0
SOURCE_PROGRESS_TOTAL=301
AGGREGATE_HEADER=$'suite	target	actual_status	expected_status	exit_status	loop	raw_output'
MATRIX_HEADER=$'suite	target	expected_status'
RESOURCE_EVENTS_HEADER=$'suite	target	event	exit_status	systemd_result	exec_main_code	exec_main_status	memory_max_mb	memory_swap_max	raw_output	unit'
RUN_STATE_FILE=
CURRENT_TARGET_FILE=
CURRENT_SYSTEMD_UNIT=
CURRENT_SYSTEMD_WAIT_PID=
CURRENT_SUITE=
CURRENT_TARGET=
CURRENT_RAW=
CURRENT_STARTED_AT=
SOURCE_RUN_INTERRUPTING=0

if [[ "$RUNNER_PATH" != "$ROOT_DIR/$RUNNER_REL" ]]; then
  echo "error: resolved runner path is outside the expected repository location: $RUNNER_PATH" >&2
  exit 2
fi

GIT_CMD=()
GIT_ROOT_REPORTED=
if [[ "$ROOT_DIR" == /mnt/?/* ]] \
    && [[ -x /mnt/d/Git/cmd/git.exe ]] \
    && command -v wslpath >/dev/null 2>&1; then
  GIT_ROOT_WINDOWS="$(wslpath -w "$ROOT_DIR")"
  GIT_CMD=(/mnt/d/Git/cmd/git.exe -C "$GIT_ROOT_WINDOWS")
  GIT_ROOT_REPORTED="$(wslpath -u "$("${GIT_CMD[@]}" rev-parse --show-toplevel)")"
else
  command -v git >/dev/null 2>&1 || { echo "error: required command not found: git" >&2; exit 2; }
  GIT_CMD=("$(command -v git)" -c "safe.directory=$ROOT_DIR" -C "$ROOT_DIR")
  GIT_ROOT_REPORTED="$("${GIT_CMD[@]}" rev-parse --show-toplevel)"
fi
if [[ "$(readlink -f "$GIT_ROOT_REPORTED")" != "$ROOT_DIR" ]]; then
  echo "error: runner-derived root and Git root differ" >&2
  exit 2
fi

COMMON_REQUIRED_COMMANDS=(awk sed grep sort find xargs sha256sum head tail cut wc tr cmp diff mktemp cp chmod rm mkdir python3)
for common_command in "${COMMON_REQUIRED_COMMANDS[@]}"; do
  command -v "$common_command" >/dev/null 2>&1 || {
    echo "error: required command not found: $common_command" >&2
    exit 2
  }
done
PYTHON_CMD="$(command -v python3)"

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

git_cmd() { "${GIT_CMD[@]}" "$@" </dev/null; }

validate_positive_mb() {
  local value="$1"
  [[ "$value" =~ ^[0-9]+$ && "$value" -ge 16 ]] || {
    echo "error: --memory-max-mb must be an integer >= 16: $value" >&2
    return 1
  }
}

iso_timestamp() { date -Is; }

atomic_write() {
  local destination="$1" tmp
  tmp="$(mktemp "${destination}.tmp.XXXXXX")"
  cat > "$tmp"
  mv -f "$tmp" "$destination"
}

write_run_state() {
  local state="$1"; shift
  [[ -n "$RUN_STATE_FILE" ]] || return 0
  {
    printf '%s\n' "$state"
    printf 'updated_at=%s\n' "$(iso_timestamp)"
    printf 'memory_max_mb=%s\n' "$TAMARIN_MEMORY_MAX_MB"
    printf 'memory_swap_max=0\n'
    for item in "$@"; do printf '%s\n' "$item"; done
  } | atomic_write "$RUN_STATE_FILE"
}

write_current_target() {
  local phase="$1" suite="$2" target="$3" raw="$4" pid="$5" unit="$6" exit_status="${7:-}" event="${8:-}"
  [[ -n "$CURRENT_TARGET_FILE" ]] || return 0
  {
    printf 'phase=%s\n' "$phase"
    printf 'updated_at=%s\n' "$(iso_timestamp)"
    printf 'suite=%s\n' "$suite"
    printf 'target=%s\n' "$target"
    printf 'pid=%s\n' "${pid:-none}"
    printf 'systemd_unit=%s\n' "${unit:-none}"
    printf 'raw_output=%s\n' "$raw"
    [[ -z "$CURRENT_STARTED_AT" ]] || printf 'started_at=%s\n' "$CURRENT_STARTED_AT"
    [[ -z "$exit_status" ]] || printf 'exit_status=%s\n' "$exit_status"
    [[ -z "$event" ]] || printf 'event=%s\n' "$event"
  } | atomic_write "$CURRENT_TARGET_FILE"
}

append_resource_event() {
  local out="$1" suite="$2" target="$3" event="$4" exit_status="$5" result="$6" code="$7" status="$8" raw="$9" unit="${10}"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t0\t%s\t%s\n' \
    "$suite" "$target" "$event" "$exit_status" "${result:-unknown}" "${code:-unknown}" \
    "${status:-unknown}" "$TAMARIN_MEMORY_MAX_MB" "$raw" "$unit" >> "$out/resource-events.tsv"
}

unit_safe_name() {
  local suite="$1" target="$2" cleaned
  cleaned="$(printf '%s-%s' "$suite" "$target" | tr -c 'A-Za-z0-9_' '-' | cut -c1-80)"
  printf 'kwaay-m4-%s-%s-%s' "$$" "$SOURCE_PROGRESS_CURRENT" "$cleaned"
}

extract_proverif_version_line() {
  grep -E '^[Pp]ro[Vv]erif[[:space:]][0-9]' "$@" 2>/dev/null | head -n 1
}

write_proverif_version_probe() {
  local stdout stderr status=0 version bad_fd=false
  stdout="$(mktemp)"; stderr="$(mktemp)"
  "${PROVERIF_CMD[@]}" -version </dev/null >"$stdout" 2>"$stderr" || status=$?
  printf 'proverif_version_probe_status=%s\n' "$status"
  version="$(extract_proverif_version_line "$stdout" || true)"
  [[ -n "$version" ]] || version="$(extract_proverif_version_line "$stderr" || true)"
  if [[ -n "$version" ]]; then
    printf 'proverif_version=%s\n' "$version"
  else
    printf 'proverif_version_probe_result=unavailable\n'
  fi
  if grep -Fq 'read failed 9: Bad file descriptor' "$stdout" "$stderr" 2>/dev/null; then bad_fd=true; fi
  printf 'proverif_version_probe_bad_fd=%s\n' "$bad_fd"
  rm -f "$stdout" "$stderr"
}

require_resource_isolation() {
  validate_positive_mb "$TAMARIN_MEMORY_MAX_MB" || return 1
  command -v systemd-run >/dev/null 2>&1 || { echo "error: systemd-run required for per-target memory limits" >&2; return 1; }
  command -v systemctl >/dev/null 2>&1 || { echo "error: systemctl required for per-target memory diagnostics" >&2; return 1; }
  systemctl --user show-environment >/dev/null 2>&1 || {
    echo "error: systemd --user is unavailable; cannot apply per-target cgroup memory limits" >&2
    return 1
  }
  local unit status result
  unit="kwaay-m4-preflight-$$"
  systemd-run --user --wait --quiet --unit="$unit" \
    --property=MemoryAccounting=yes --property=MemoryMax=32M --property=MemorySwapMax=0 \
    --property=StandardInput=null --property=StandardOutput=null --property=StandardError=null \
    /usr/bin/python3 -c 'a=bytearray(256*1024*1024); print(len(a))' >/dev/null 2>&1 || status=$?
  result="$(systemctl --user show "$unit.service" -p Result --value 2>/dev/null || true)"
  systemctl --user reset-failed "$unit.service" >/dev/null 2>&1 || true
  if [[ "${status:-0}" -eq 0 || "$result" != oom-kill ]]; then
    echo "error: systemd --user MemoryMax/MemorySwapMax preflight did not produce cgroup oom-kill" >&2
    return 1
  fi
}

LAST_SYSTEMD_RESULT=unknown
LAST_EXEC_MAIN_CODE=unknown
LAST_EXEC_MAIN_STATUS=unknown

normalize_systemd_exit_status() {
  local runner_exit="$1" code="$2" status="$3"
  if [[ "$code" == 1 && "$status" =~ ^[0-9]+$ ]]; then
    printf '%s' "$status"
  elif [[ "$code" == 2 && "$status" =~ ^[0-9]+$ ]]; then
    printf '%s' $((128 + status))
  else
    printf '%s' "$runner_exit"
  fi
}

run_limited_tamarin_command() {
  local out="$1" suite="$2" target="$3" raw="$4" unit exit_code=0
  shift 4
  : > "$raw"
  unit="$(unit_safe_name "$suite" "$target")"
  LAST_SYSTEMD_RESULT=unknown
  LAST_EXEC_MAIN_CODE=unknown
  LAST_EXEC_MAIN_STATUS=unknown
  CURRENT_SYSTEMD_UNIT="$unit"
  CURRENT_SUITE="$suite"
  CURRENT_TARGET="$target"
  CURRENT_RAW="$raw"
  CURRENT_STARTED_AT="$(iso_timestamp)"
  systemd-run --user --wait --quiet --unit="$unit" \
    --setenv=PATH="$PATH" --setenv=HOME="${HOME:-$ROOT_DIR}" \
    --property=MemoryAccounting=yes --property=MemoryMax="${TAMARIN_MEMORY_MAX_MB}M" --property=MemorySwapMax=0 \
    --property=KillMode=control-group --property=StandardInput=null \
    --property="StandardOutput=file:$raw" --property="StandardError=append:$raw" \
    "$@" &
  CURRENT_SYSTEMD_WAIT_PID=$!
  write_current_target running "$suite" "$target" "$raw" "$CURRENT_SYSTEMD_WAIT_PID" "$unit"
  wait "$CURRENT_SYSTEMD_WAIT_PID" || exit_code=$?
  LAST_SYSTEMD_RESULT="$(systemctl --user show "$unit.service" -p Result --value 2>/dev/null || true)"
  LAST_EXEC_MAIN_CODE="$(systemctl --user show "$unit.service" -p ExecMainCode --value 2>/dev/null || true)"
  LAST_EXEC_MAIN_STATUS="$(systemctl --user show "$unit.service" -p ExecMainStatus --value 2>/dev/null || true)"
  exit_code="$(normalize_systemd_exit_status "$exit_code" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS")"
  systemctl --user reset-failed "$unit.service" >/dev/null 2>&1 || true
  CURRENT_SYSTEMD_WAIT_PID=
  CURRENT_SYSTEMD_UNIT=
  return "$exit_code"
}

classify_target_event() {
  local exit_code="$1" result="$2" code="$3" status="$4"
  if [[ "$result" == oom-kill ]]; then printf 'oom_kill'
  elif [[ "$code" == 2 && "$status" == 9 ]]; then printf 'sigkill'
  elif [[ "$exit_code" == 124 ]]; then printf 'timeout'
  elif [[ "$exit_code" == 0 ]]; then printf 'none'
  else printf 'nonzero_exit'; fi
}

terminate_current_proof() {
  local reason="$1"
  if [[ -n "$CURRENT_SYSTEMD_UNIT" ]]; then
    systemctl --user kill --kill-whom=all "$CURRENT_SYSTEMD_UNIT.service" >/dev/null 2>&1 || true
    systemctl --user stop "$CURRENT_SYSTEMD_UNIT.service" >/dev/null 2>&1 || true
  fi
  if [[ -n "$CURRENT_SYSTEMD_WAIT_PID" ]]; then wait "$CURRENT_SYSTEMD_WAIT_PID" >/dev/null 2>&1 || true; fi
  [[ -n "$CURRENT_SYSTEMD_UNIT" ]] && systemctl --user reset-failed "$CURRENT_SYSTEMD_UNIT.service" >/dev/null 2>&1 || true
  write_current_target interrupted "${CURRENT_SUITE:-unknown}" "${CURRENT_TARGET:-unknown}" \
    "${CURRENT_RAW:-unknown}" "${CURRENT_SYSTEMD_WAIT_PID:-none}" "${CURRENT_SYSTEMD_UNIT:-none}" "" "$reason"
}

handle_source_interrupt() {
  local signal_name="$1" exit_code="$2" run_dir
  [[ "$SOURCE_RUN_INTERRUPTING" -eq 0 ]] || exit "$exit_code"
  SOURCE_RUN_INTERRUPTING=1
  terminate_current_proof "$signal_name"
  if [[ -n "$RUN_STATE_FILE" ]]; then
    run_dir="$(dirname "$RUN_STATE_FILE")"
    rm -f "$run_dir/source-run-status.txt" "$run_dir/SHA256SUMS.txt"
  fi
  write_run_state INTERRUPTED "signal=$signal_name" "exit_code=$exit_code" \
    "last_suite=${CURRENT_SUITE:-unknown}" "last_target=${CURRENT_TARGET:-unknown}" \
    "sigkill_note=SIGKILL and whole-WSL OOM shutdown cannot be trapped; per-target cgroup isolation is the primary protection"
  exit "$exit_code"
}

emit_suite_matrix() {
  local suite="$1" array_name="$2" map_name="$3" target
  local -n targets="$array_name" expected_map="$map_name"
  for target in "${targets[@]}"; do
    printf '%s\t%s\t%s\n' "$suite" "$target" "${expected_map[$target]}"
  done
}

emit_proverif_matrix() {
  local suite="$1" array_name="$2" target
  local -n targets="$array_name"
  for target in "${targets[@]}"; do printf '%s\t%s\tMATCH\n' "$suite" "$target"; done
}

emit_canonical_matrix() {
  printf '%s\n' "$MATRIX_HEADER"
  emit_suite_matrix combined-replay COMBINED_REPLAY_TARGETS EXPECT_COMBINED_REPLAY
  emit_suite_matrix combined-impact COMBINED_IMPACT_TARGETS EXPECT_COMBINED_IMPACT
  emit_suite_matrix original-replay ORIGINAL_REPLAY_TARGETS EXPECT_ORIGINAL_REPLAY
  emit_suite_matrix hmac-replay HMAC_REPLAY_TARGETS EXPECT_HMAC_REPLAY
  emit_suite_matrix original-impact ORIGINAL_IMPACT_TARGETS EXPECT_ORIGINAL_IMPACT
  emit_suite_matrix fixed-replay FIXED_REPLAY_TARGETS EXPECT_FIXED_REPLAY
  emit_suite_matrix fixed-impact FIXED_IMPACT_TARGETS EXPECT_FIXED_IMPACT
  emit_suite_matrix v6 V6_TARGETS EXPECT_V6
  emit_suite_matrix v7 V7_TARGETS EXPECT_V7
  emit_proverif_matrix proverif-original PROVERIF_ORIGINAL_TARGETS
  emit_proverif_matrix proverif-hmac PROVERIF_HMAC_TARGETS
}

validate_canonical_matrix() {
  local matrix="${1:-}" own=0 rows unique expected_counts actual suite count failures=0
  if [[ -z "$matrix" ]]; then matrix="$(mktemp)"; emit_canonical_matrix > "$matrix"; own=1; fi
  [[ "$(head -n1 "$matrix")" == "$MATRIX_HEADER" ]] || { echo "error: canonical matrix header mismatch" >&2; failures=1; }
  rows="$(awk -F '\t' 'NR>1 {if(NF!=3) bad=1; n++} END{if(bad) exit 1; print n+0}' "$matrix")" || failures=1
  [[ "$rows" == 301 ]] || { echo "error: canonical matrix has $rows rows, expected 301" >&2; failures=1; }
  unique="$(awk -F '\t' 'NR>1 {print $1 "\t" $2}' "$matrix" | LC_ALL=C sort -u | wc -l | tr -d ' ')"
  [[ "$unique" == 301 ]] || { echo "error: canonical suite/target combinations are not unique" >&2; failures=1; }
  expected_counts=$'combined-replay\t38\ncombined-impact\t62\noriginal-replay\t18\nhmac-replay\t18\noriginal-impact\t37\nfixed-replay\t30\nfixed-impact\t53\nv6\t16\nv7\t24\nproverif-original\t2\nproverif-hmac\t3'
  actual="$(awk -F '\t' 'NR>1 {n[$1]++} END{for(s in n) print s "\t" n[s]}' "$matrix" | LC_ALL=C sort)"
  [[ "$actual" == "$(printf '%s\n' "$expected_counts" | LC_ALL=C sort)" ]] || {
    echo "error: canonical suite counts differ from the frozen 301-target matrix" >&2; failures=1; }
  if awk -F '\t' 'NR>1 && $3!="verified" && $3!="falsified" && $3!="MATCH" {exit 1}' "$matrix"; then :; else
    echo "error: invalid expected status in canonical matrix" >&2; failures=1
  fi
  [[ "$own" -eq 0 ]] || rm -f "$matrix"
  [[ "$failures" -eq 0 ]]
}

validate_source_matrix() {
  local aggregate="$1" canonical actual rows unique failures=0
  [[ -f "$aggregate" ]] || { echo "error: missing aggregate: $aggregate" >&2; return 1; }
  [[ "$(head -n1 "$aggregate")" == "$AGGREGATE_HEADER" ]] || {
    echo "error: aggregate header mismatch: $aggregate" >&2; return 1; }
  rows="$(awk -F '\t' 'NR>1 {if(NF!=7) bad=1; n++} END{if(bad) exit 1; print n+0}' "$aggregate")" || {
    echo "error: malformed aggregate row" >&2; return 1; }
  [[ "$rows" == 301 ]] || { echo "error: aggregate has $rows rows, expected 301" >&2; failures=1; }
  unique="$(awk -F '\t' 'NR>1 {print $1 "\t" $2}' "$aggregate" | LC_ALL=C sort -u | wc -l | tr -d ' ')"
  [[ "$unique" == 301 ]] || { echo "error: duplicate suite/target in aggregate" >&2; failures=1; }
  canonical="$(mktemp)"; actual="$(mktemp)"
  emit_canonical_matrix | tail -n +2 | LC_ALL=C sort > "$canonical"
  awk -F '\t' 'NR>1 {print $1 "\t" $2 "\t" $4}' "$aggregate" | LC_ALL=C sort > "$actual"
  if ! cmp -s "$canonical" "$actual"; then
    echo "error: aggregate has missing, extra, or expected-status-drifted targets" >&2
    diff -u "$canonical" "$actual" >&2 || true
    failures=1
  fi
  rm -f "$canonical" "$actual"
  if awk -F '\t' 'NR>1 && $3!="verified" && $3!="falsified" && $3!="MATCH" && $3!="nonterminal" {exit 1}' "$aggregate"; then :; else
    echo "error: invalid actual status in aggregate" >&2; failures=1
  fi
  [[ "$failures" -eq 0 ]]
}

source_has_nonterminal() { awk -F '\t' 'NR>1 && $3=="nonterminal" {found=1} END{exit(found?0:1)}' "$1"; }

unexpected_git_status() {
  git_cmd status --porcelain=v1 --untracked-files=all | awk -v log_path="$LOG_REL" '
    {
      path=substr($0,4)
      if (path==log_path || index(path,log_path "/")==1) next
      print
    }
  '
}

verify_repo_clean_except_logs() {
  local status
  status="$(unexpected_git_status)"
  [[ -z "$status" ]] || { echo "error: repository changes outside $LOG_REL" >&2; printf '%s\n' "$status" >&2; return 1; }
}

BOUND_PATHS=("$RUNNER_REL" "$COMBINED_REPLAY_REL" "$COMBINED_IMPACT_REL" "${FROZEN_PATHS[@]}")

verify_current_binding_state() {
  local path
  verify_repo_clean_except_logs || return 1
  for path in "${BOUND_PATHS[@]}"; do
    [[ -f "$ROOT_DIR/$path" ]] || { echo "error: bound input missing: $path" >&2; return 1; }
    git_cmd cat-file -e "HEAD:$path" 2>/dev/null || { echo "error: bound input is not tracked at HEAD: $path" >&2; return 1; }
  done
  git_cmd diff --quiet HEAD -- "${BOUND_PATHS[@]}" || {
    echo "error: runner/model/frozen input differs from current HEAD" >&2; return 1; }
  verify_frozen_inputs
}

write_binding() {
  local destination="$1" path
  {
    printf 'key\tvalue\n'
    printf 'git_head\t%s\n' "$(git_cmd rev-parse HEAD)"
    printf 'git_tree\t%s\n' "$(git_cmd show -s --format=%T HEAD)"
    printf 'git_branch\t%s\n' "$(git_cmd branch --show-current)"
    for path in "${BOUND_PATHS[@]}"; do
      printf 'blob:%s\t%s\n' "$path" "$(git_cmd rev-parse "HEAD:$path")"
      printf 'sha256:%s\t%s\n' "$path" "$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    done
  } > "$destination"
}

validate_binding_against_current() {
  local run="$1" current
  [[ -f "$run/binding.tsv" ]] || { echo "error: missing binding.tsv in $run" >&2; return 1; }
  verify_current_binding_state || return 1
  current="$(mktemp)"; write_binding "$current"
  if ! cmp -s "$current" "$run/binding.tsv"; then
    echo "error: current Commit A binding differs from source run: $run" >&2
    diff -u "$run/binding.tsv" "$current" >&2 || true
    rm -f "$current"; return 1
  fi
  rm -f "$current"
}

validate_log_top_level_at() {
  local directory="$1" mode="$2" entries allowed entry
  [[ -d "$directory" ]] || { echo "error: missing log directory: $directory" >&2; return 1; }
  case "$mode" in
    run2) allowed=$'source-run1' ;;
    assemble) allowed=$'source-run1\nsource-run2' ;;
    *) return 2 ;;
  esac
  entries="$(find "$directory" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort)"
  while IFS= read -r entry; do
    [[ -z "$entry" ]] && continue
    grep -Fxq "$entry" <<<"$allowed" || { echo "error: unknown or stale top-level log artifact: $entry" >&2; return 1; }
  done <<<"$entries"
  [[ -d "$directory/source-run1" ]] || { echo "error: legal source-run1 is required" >&2; return 1; }
  if [[ "$mode" == run2 && "$entries" != source-run1 ]]; then
    echo "error: Run 2 requires source-run1 to be the only top-level entry" >&2; return 1
  fi
}

validate_log_top_level() { validate_log_top_level_at "$LOG_DIR" "$1"; }

make_manifest() {
  local out="$1"
  (cd "$out" && find . -type f ! -path './SHA256SUMS.txt' -printf '%P\0' | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS.txt)
  validate_manifest "$out"
}

validate_manifest() {
  local out="$1" listed actual failures=0
  [[ -d "$out" && -f "$out/SHA256SUMS.txt" ]] || { echo "error: missing source manifest: $out" >&2; return 1; }
  listed="$(mktemp)"; actual="$(mktemp)"
  awk 'length($1)==64 {line=$0; sub(/^[0-9a-fA-F]{64}  ?/,"",line); print line}' "$out/SHA256SUMS.txt" | LC_ALL=C sort > "$listed"
  (cd "$out" && find . -type f ! -path './SHA256SUMS.txt' -printf '%P\n' | LC_ALL=C sort) > "$actual"
  if ! cmp -s "$listed" "$actual"; then
    echo "error: manifest inventory mismatch in $out" >&2
    diff -u "$listed" "$actual" >&2 || true
    failures=1
  fi
  if [[ "$(wc -l < "$listed" | tr -d ' ')" != "$(LC_ALL=C sort -u "$listed" | wc -l | tr -d ' ')" ]]; then
    echo "error: duplicate manifest path in $out" >&2; failures=1
  fi
  if ! (cd "$out" && sha256sum -c SHA256SUMS.txt >/dev/null); then
    echo "error: sha256sum verification failed in $out" >&2; failures=1
  fi
  rm -f "$listed" "$actual"
  [[ "$failures" -eq 0 ]]
}

resolve_proverif() {
  PROVERIF_CMD=(); PROVERIF_NEEDS_WIN_PATH=0
  if command -v proverif >/dev/null 2>&1; then
    PROVERIF_CMD=("$(command -v proverif)")
  elif command -v proverif.exe >/dev/null 2>&1; then
    PROVERIF_CMD=("$(command -v proverif.exe)"); PROVERIF_NEEDS_WIN_PATH=1
  elif [[ -x /mnt/d/Proverif/proverif2.05/proverif.exe ]]; then
    PROVERIF_CMD=(/mnt/d/Proverif/proverif2.05/proverif.exe); PROVERIF_NEEDS_WIN_PATH=1
  else
    echo "error: ProVerif not found" >&2; return 1
  fi
}

resolve_formal_tools() {
  local command_name
  for command_name in tamarin-prover maude cpp timeout uname python3; do
    command -v "$command_name" >/dev/null 2>&1 || { echo "error: required command not found: $command_name" >&2; return 1; }
  done
  TAMARIN_CMD="$(command -v tamarin-prover)"
  MAUDE_CMD="$(command -v maude)"
  CPP_CMD="$(command -v cpp)"
  TIMEOUT_CMD="$(command -v timeout)"
  PYTHON_CMD="$(command -v python3)"
  resolve_proverif
  local help
  help="$("$TAMARIN_CMD" --help 2>&1)"
  grep -q -- '--output-json' <<<"$help" && grep -q -- '--output-dot' <<<"$help" || {
    echo "error: Tamarin does not advertise JSON/DOT output" >&2; return 1; }
}

tool_input_path() {
  local path="$1"
  if [[ "$PROVERIF_NEEDS_WIN_PATH" -eq 1 ]]; then
    command -v wslpath >/dev/null 2>&1 || { echo "error: wslpath required for Windows ProVerif" >&2; return 1; }
    wslpath -w "$path"
  else
    printf '%s\n' "$path"
  fi
}

print_command() { local label="$1"; shift; printf '%s:' "$label"; printf ' %q' "$@"; printf '\n'; }
stage_notice() { printf '[stage] %s\n' "$1" >&2; }
report_source_progress() {
  local suite="$1" target="$2" status="$3"
  SOURCE_PROGRESS_CURRENT=$((SOURCE_PROGRESS_CURRENT + 1))
  printf '[%d/%d] %s / %s -> %s\n' "$SOURCE_PROGRESS_CURRENT" "$SOURCE_PROGRESS_TOTAL" \
    "$suite" "$target" "$status" >&2
}

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

project_impact_rule() {
  local name="$1" source="$2" destination="$3"
  extract_block rule "$name" "$source" | normalize_text > "$destination"
  case "$name" in
    ProcessSlot1|ProcessSlot2)
      sed -E -i \
        -e 's/,Fr\(~aid\)//' \
        -e 's/,AcceptOutputCreated\(~aid,\$B,\$A,bid,idx,rst,m,sid,k\)//' \
        -e 's/,AcceptedOutput\(~aid,\$B,\$A,bid,idx,rst,m,sid,k\)//' \
        "$destination"
      ;;
    CompleteBatch)
      sed -E -i \
        -e 's/,ConsumerStarted\(\$B,bid,rst\)//' \
        -e 's/,ConsumerStage0\(\$B,bid,rst\)//' \
        "$destination"
      ;;
  esac
}

compare_replay_impact_lower() {
  local failures=0 name a b functions_a functions_b
  functions_a="$(mktemp)"; functions_b="$(mktemp)"
  awk '{sub(/\r$/,"")} /^functions:/{p=1} p{print} p && /^$/{exit}' "$ROOT_DIR/$COMBINED_REPLAY_REL" | normalize_text > "$functions_a"
  awk '{sub(/\r$/,"")} /^functions:/{p=1} p{print} p && /^$/{exit}' "$ROOT_DIR/$COMBINED_IMPACT_REL" | normalize_text > "$functions_b"
  cmp -s "$functions_a" "$functions_b" || { echo "error: combined replay/impact functions differ" >&2; failures=1; }
  rm -f "$functions_a" "$functions_b"

  for name in Inequality TagInequality; do
    a="$(mktemp)"; b="$(mktemp)"
    extract_block restriction "$name" "$ROOT_DIR/$COMBINED_REPLAY_REL" | normalize_text > "$a"
    extract_block restriction "$name" "$ROOT_DIR/$COMBINED_IMPACT_REL" | normalize_text > "$b"
    cmp -s "$a" "$b" || { echo "error: combined restriction mismatch: $name" >&2; failures=1; }
    rm -f "$a" "$b"
  done

  for name in InitReceiverState InitSenderState SenderCreatesConfirmedMessage CreateBatch \
      AddSlot1 AddSlot2 SealBatch RejectDuplicateBatch PassDistinctBatch \
      DetectHmacMismatchSlot1 DetectHmacMismatchSlot2 CloseHmacRejectSlot1 CloseHmacRejectSlot2 \
      FailSlot1 FailSlot2 CompromiseReceiverState CompromiseActiveReceiverState CompromiseSenderState; do
    compare_rule_normalized "$name" "$ROOT_DIR/$COMBINED_REPLAY_REL" "$ROOT_DIR/$COMBINED_IMPACT_REL" || failures=1
  done
  for name in ProcessSlot1 ProcessSlot2 CompleteBatch; do
    a="$(mktemp)"; b="$(mktemp)"
    extract_block rule "$name" "$ROOT_DIR/$COMBINED_REPLAY_REL" | normalize_text > "$a"
    project_impact_rule "$name" "$ROOT_DIR/$COMBINED_IMPACT_REL" "$b"
    cmp -s "$a" "$b" || {
      echo "error: combined lower-layer projection mismatch: $name" >&2
      diff -u "$a" "$b" >&2 || true
      failures=1
    }
    rm -f "$a" "$b"
  done
  for name in "${COMBINED_REPLAY_TARGETS[@]}"; do
    compare_formula_exact "$name" "$ROOT_DIR/$COMBINED_REPLAY_REL" "$ROOT_DIR/$COMBINED_IMPACT_REL" || failures=1
  done
  [[ "$failures" -eq 0 ]]
}

static_checks() {
  local failures=0 functions_a functions_b rule
  for path in "$COMBINED_REPLAY_REL" "$COMBINED_IMPACT_REL" \
              "$COMBINED_REPLAY_README_REL" "$COMBINED_IMPACT_README_REL"; do
    [[ -f "$ROOT_DIR/$path" ]] || { echo "error: missing $path" >&2; failures=1; }
  done
  check_inventory "$ROOT_DIR/$COMBINED_REPLAY_REL" COMBINED_REPLAY_TARGETS combined_replay || failures=1
  check_inventory "$ROOT_DIR/$COMBINED_IMPACT_REL" COMBINED_IMPACT_TARGETS combined_impact || failures=1
  validate_canonical_matrix || failures=1

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
  compare_replay_impact_lower || failures=1
  verify_frozen_inputs || failures=1

  if [[ "$failures" -ne 0 ]]; then return 1; fi
  echo "consumer_rules=3/3 MATCH"
  echo "hmac_functions=MATCH"
  echo "hmac_sender_rule=MATCH"
  echo "hmac_matching_formulas=2/2 MATCH"
  echo "m3_dedup_structure=MATCH_WITH_APPROVED_TAG_PROJECTION"
  echo "alias_tokens=ABSENT"
  echo "frozen_blobs_and_sha256=MATCH"
  echo "canonical_target_matrix=301 MATCH"
  echo "combined_replay_impact_lower_layer=MATCH_WITH_NARROW_PROJECTION"
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
  local target="$1" raw="$2" exit_code="$3" matches count line
  if [[ "$exit_code" -ne 0 || ! -s "$raw" ]] || grep -q '<<loop>>' "$raw"; then
    printf 'nonterminal'; return
  fi
  matches="$(grep -E "^[[:space:]]*$target \((all-traces|exists-trace)\): (verified \([0-9]+ steps\)|falsified - (found trace|no trace found) \([0-9]+ steps\))[[:space:]]*$" "$raw" || true)"
  count="$(printf '%s\n' "$matches" | awk 'NF{n++} END{print n+0}')"
  [[ "$count" -eq 1 ]] || { printf 'nonterminal'; return; }
  line="$matches"
  if [[ "$line" == *": verified "* ]]; then printf 'verified'
  elif [[ "$line" == *": falsified - "* ]]; then printf 'falsified'
  else printf 'nonterminal'; fi
}

run_tamarin_suite() {
  local out="$1" suite="$2" model="$3" array_name="$4" map_name="$5"
  local -n targets="$array_name" expected_map="$map_name"
  local target raw raw_rel status exit_code loop event unit
  mkdir -p "$out/proofs/$suite"
  for target in "${targets[@]}"; do
    raw="$out/proofs/$suite/$target.out"; raw_rel="proofs/$suite/$target.out"; exit_code=0
    print_command "executed-proof[$suite][$target]" "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS"       "$TAMARIN_CMD" --derivcheck-timeout=0 "--prove=$target" "$model" >> "$out/commands.txt"
    run_limited_tamarin_command "$out" "$suite" "$target" "$raw"       "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "$TAMARIN_CMD" --derivcheck-timeout=0       "--prove=$target" "$model" || exit_code=$?
    status="$(parse_tamarin_result "$target" "$raw" "$exit_code")"
    loop=false; grep -q '<<loop>>' "$raw" && loop=true
    event="$(classify_target_event "$exit_code" "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS")"
    unit="$(unit_safe_name "$suite" "$target")"
    append_resource_event "$out" "$suite" "$target" "$event" "$exit_code"       "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS" "$raw_rel" "$unit"
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$status" \
      "${expected_map[$target]}" "$exit_code" "$loop" "$raw_rel" >> "$out/aggregate.tsv"
    write_current_target completed "$suite" "$target" "$raw_rel" none "$unit" "$exit_code" "$event"
    report_source_progress "$suite" "$target" "$status"
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

compare_proverif_results() {
  local actual="$1" expected="$2" cpp_exit="$3" proverif_exit="$4" actual_count expected_count
  [[ "$cpp_exit" -eq 0 && "$proverif_exit" -eq 0 && -s "$actual" && -s "$expected" ]] || return 1
  actual_count="$(wc -l < "$actual" | tr -d ' ')"; expected_count="$(wc -l < "$expected" | tr -d ' ')"
  [[ "$actual_count" -eq "$expected_count" ]] || return 1
  cmp -s "$actual" "$expected"
}

run_proverif_target() {
  local out="$1" suite="$2" target="$3" model="$4" baseline="$5"
  local generated raw raw_rel actual expected input cpp_exit=0 exit_code=0 status=nonterminal
  mkdir -p "$out/proverif/$suite/generated" "$out/proverif/$suite/out"
  generated="$out/proverif/$suite/generated/$target.pv"; raw="$out/proverif/$suite/out/$target.out"; raw_rel="proverif/$suite/out/$target.out"
  CURRENT_SUITE="$suite"; CURRENT_TARGET="$target"; CURRENT_RAW="$raw_rel"; CURRENT_STARTED_AT="$(iso_timestamp)"
  write_current_target running "$suite" "$target" "$raw_rel" runner none
  print_command "executed-cpp[$suite][$target]" "$CPP_CMD" -P -D "$target" "$model" >> "$out/commands.txt"
  "$CPP_CMD" -P -D "$target" "$model" > "$generated" 2> "$out/proverif/$suite/out/$target.cpp.err" || cpp_exit=$?
  if [[ "$cpp_exit" -eq 0 ]]; then
    input="$(tool_input_path "$generated")"
    print_command "executed-proverif[$suite][$target]" "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" \
      "${PROVERIF_CMD[@]}" "$input" >> "$out/commands.txt"
    "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "${PROVERIF_CMD[@]}" "$input" </dev/null > "$raw" 2>&1 || exit_code=$?
  else
    exit_code="$cpp_exit"; : > "$raw"
  fi
  actual="$(mktemp)"; expected="$(mktemp)"
  grep '^RESULT ' "$raw" | sed 's/\r$//' > "$actual" || true
  extract_pv_results "$baseline" "$target" > "$expected"
  if compare_proverif_results "$actual" "$expected" "$cpp_exit" "$exit_code"; then status=MATCH; fi
  rm -f "$actual" "$expected"
  printf '%s\t%s\t%s\tMATCH\t%s\tfalse\t%s\n' "$suite" "$target" "$status" "$exit_code" \
    "$raw_rel" >> "$out/aggregate.tsv"
  write_current_target completed "$suite" "$target" "$raw_rel" none none "$exit_code" none
  report_source_progress "$suite" "$target" "$status"
}

write_provenance() {
  local out="$1" run_number="$2" os_name path command_name
  os_name="$(awk -F= '$1=="PRETTY_NAME"{gsub(/^"|"$/,"",$2); print $2; exit}' /etc/os-release 2>/dev/null || true)"
  {
    echo "git_head=$(git_cmd rev-parse HEAD)"
    echo "git_tree=$(git_cmd show -s --format=%T HEAD)"
    echo "git_branch=$(git_cmd branch --show-current)"
    echo "os=${os_name:-unknown}"
    echo "uname=$(uname -a)"
    echo "git_executable=${GIT_CMD[0]}"
    echo "tamarin_executable=$TAMARIN_CMD"
    echo "maude_executable=$MAUDE_CMD"
    echo "proverif_executable=${PROVERIF_CMD[0]}"
    echo "cpp_executable=$CPP_CMD"
    echo "timeout_executable=$TIMEOUT_CMD"
    echo "python_executable=$PYTHON_CMD"
    echo "uname_executable=$(command -v uname)"
    echo "bash_executable=$(command -v bash)"
    if command -v wslpath >/dev/null 2>&1; then echo "wslpath_executable=$(command -v wslpath)"; fi
    for command_name in "${COMMON_REQUIRED_COMMANDS[@]}"; do
      printf 'resolved_executable[%s]=%s\n' "$command_name" "$(command -v "$command_name")"
    done
    echo "proof_timeout_seconds=$PROOF_TIMEOUT_SECONDS"
    echo "tamarin_memory_max_mb=$TAMARIN_MEMORY_MAX_MB"
    echo "tamarin_memory_swap_max=0"
    echo "tamarin_memory_limit_mechanism=systemd-run --user transient service cgroup"
    echo "source_run_number=$run_number"
    printf 'exact_runner_command='; printf '%q ' "$0" --memory-max-mb "$TAMARIN_MEMORY_MAX_MB" --source-run "$run_number"; echo
    echo "binding_file=binding.tsv"
    for path in "${BOUND_PATHS[@]}"; do
      printf 'bound_blob[%s]=%s\n' "$path" "$(git_cmd rev-parse "HEAD:$path")"
      printf 'bound_sha256[%s]=%s\n' "$path" "$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')"
    done
    "$TAMARIN_CMD" --version 2>&1 | sed 's/^/tamarin_version=/'
    "$MAUDE_CMD" --version 2>&1 | head -n3 | sed 's/^/maude_version=/'
    write_proverif_version_probe
    "$CPP_CMD" --version 2>&1 | head -n1 | sed 's/^/cpp_version=/'
    "$TIMEOUT_CMD" --version 2>&1 | head -n1 | sed 's/^/timeout_version=/'
    "$PYTHON_CMD" --version 2>&1 | sed 's/^/python_version=/'
  } > "$out/provenance.txt"
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
  local out="$1" path
  printf 'path\tblob\tsha256\n' > "$out/frozen-inputs.tsv"
  for path in "${FROZEN_PATHS[@]}"; do
    printf '%s\t%s\t%s\n' "$path" "$(git_cmd rev-parse "HEAD:$path")" \
      "$(sha256sum "$ROOT_DIR/$path" | awk '{print $1}')" >> "$out/frozen-inputs.tsv"
  done
}

terminal_status() { [[ "$1" == verified || "$1" == falsified || "$1" == MATCH ]]; }
event_count() { LC_ALL=C grep -ao -F "$2(" "$1" | wc -l | tr -d ' '; }
unique_event_argument_count() {
  local file="$1" event="$2" argument="$3"
  LC_ALL=C grep -ao -E "$event\([^)]*\)" "$file" \
    | sed -E "s/^$event\\(//; s/\\)$//" \
    | awk -F ',' -v field="$argument" '{value=$field; gsub(/[[:space:]\\\\]/,"",value); if(value!="") print value}' \
    | LC_ALL=C sort -u | wc -l | tr -d ' '
}

validate_json_trace() {
  "$PYTHON_CMD" - "$1" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        value = json.load(handle)
except (OSError, UnicodeError, json.JSONDecodeError):
    raise SystemExit(1)
if not isinstance(value, dict):
    raise SystemExit(1)
graphs = value.get("graphs")
if not isinstance(graphs, list) or not graphs:
    raise SystemExit(1)
PY
}

validate_dot_digraph() {
  "$PYTHON_CMD" - "$1" <<'PY'
import re
import sys

try:
    text = open(sys.argv[1], "r", encoding="utf-8").read()
except (OSError, UnicodeError):
    raise SystemExit(1)
if not re.match(r"^\s*(?:strict\s+)?digraph(?:\s+(?:[A-Za-z_][A-Za-z0-9_]*|\"(?:[^\"\\]|\\.)*\"))?\s*\{", text):
    raise SystemExit(1)
depth = 0
opened = False
in_string = False
escaped = False
line_comment = False
block_comment = False
i = 0
last_close = -1
while i < len(text):
    char = text[i]
    nxt = text[i + 1] if i + 1 < len(text) else ""
    if line_comment:
        if char == "\n":
            line_comment = False
    elif block_comment:
        if char == "*" and nxt == "/":
            block_comment = False
            i += 1
    elif in_string:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            in_string = False
    elif char == '"':
        in_string = True
    elif char == "/" and nxt == "/":
        line_comment = True
        i += 1
    elif char == "/" and nxt == "*":
        block_comment = True
        i += 1
    elif char == "{":
        depth += 1
        opened = True
    elif char == "}":
        depth -= 1
        if depth < 0:
            raise SystemExit(1)
        if depth == 0:
            last_close = i
    i += 1
if not opened or depth != 0 or in_string or block_comment:
    raise SystemExit(1)
if text[last_close + 1:].strip().strip(";").strip():
    raise SystemExit(1)
PY
}

trace_raw_matches_theory() {
  local raw="$1" theory="$2" line trimmed
  [[ -s "$raw" && -n "$theory" ]] || return 1
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    trimmed="$(printf '%s' "$line" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
    [[ "$trimmed" == "[Theory $theory]" || "$trimmed" == "theory $theory" ]] && return 0
  done < "$raw"
  return 1
}

formula_digest_for() { extract_block lemma "$2" "$1" | normalize_text | sha256sum | awk '{print $1}'; }

validate_trace_formula_contract() {
  local label="$1" model="$2" lemma="$3" recorded_digest="$4" actual_digest formula
  actual_digest="$(formula_digest_for "$model" "$lemma")"
  [[ -n "$recorded_digest" && "$actual_digest" == "$recorded_digest" ]] || return 1
  formula="$(extract_block lemma "$lemma" "$model" | normalize_text)"
  case "$label" in
    slot1-mismatch) [[ "$formula" == *'#p<#hf'* && "$formula" == *'#hf<#bf'* ]] ;;
    slot2-mismatch) [[ "$formula" == *'#r1<#hf'* && "$formula" == *'#hf<#bf'* ]] ;;
    *) return 0 ;;
  esac
}

validate_trace_artifacts() {
  local label="$1" model="$2" lemma="$3" raw="$4" json="$5" dot="$6" exit_code="$7" recorded_digest="$8"
  local theory failures=0 event
  theory="$(awk '/^theory[[:space:]]+/{print $2; exit}' "$model")"
  [[ "$exit_code" -eq 0 ]] || return 1
  [[ -s "$raw" && -s "$json" && -s "$dot" ]] || failures=1
  [[ "$(parse_tamarin_result "$lemma" "$raw" "$exit_code")" == verified ]] || failures=1
  trace_raw_matches_theory "$raw" "$theory" || failures=1
  grep -Fq '<<loop>>' "$raw" && failures=1
  validate_trace_formula_contract "$label" "$model" "$lemma" "$recorded_digest" || failures=1
  validate_json_trace "$json" || failures=1
  validate_dot_digraph "$dot" || failures=1
  case "$label" in
    duplicate)
      for event in DuplicateDetected BatchFail BatchClosed ConsumeReceiverState; do [[ "$(event_count "$dot" "$event")" -ge 1 ]] || failures=1; done
      [[ "$(event_count "$dot" ConfirmedReceiverAccept)" -eq 0 ]] || failures=1
      ;;
    normal-replay)
      [[ "$(unique_event_argument_count "$dot" ConfirmedSend 3)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" DedupPassed)" -ge 1 ]] || failures=1
      [[ "$(event_count "$dot" HmacValidated)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" ConfirmedReceiverAccept)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" BatchComplete)" -ge 1 ]] || failures=1
      ;;
    slot1-mismatch)
      [[ "$(event_count "$dot" HmacValidationFailed)" -ge 1 ]] || failures=1
      [[ "$(event_count "$dot" BatchFail)" -ge 1 ]] || failures=1
      [[ "$(event_count "$dot" ConfirmedReceiverAccept)" -eq 0 ]] || failures=1
      ;;
    slot2-mismatch)
      [[ "$(event_count "$dot" ConfirmedReceiverAccept)" -ge 1 ]] || failures=1
      [[ "$(event_count "$dot" HmacValidationFailed)" -ge 1 ]] || failures=1
      [[ "$(event_count "$dot" BatchFail)" -ge 1 ]] || failures=1
      for event in BatchComplete ConsumerStarted InstallFromAccept; do [[ "$(event_count "$dot" "$event")" -eq 0 ]] || failures=1; done
      ;;
    normal-consumer)
      [[ "$(unique_event_argument_count "$dot" AcceptOutputCreated 1)" -ge 2 ]] || failures=1
      [[ "$(unique_event_argument_count "$dot" InstallFromAccept 3)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" AcceptOutputCreated)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" InstallFromAccept)" -ge 2 ]] || failures=1
      [[ "$(event_count "$dot" ConsumerComplete)" -ge 1 ]] || failures=1
      ;;
    *) failures=1 ;;
  esac
  [[ "$failures" -eq 0 ]]
}

run_trace() {
  local out="$1" label="$2" model_rel="$3" lemma="$4" dir raw json dot exit_code=0 result=FAIL suite digest raw_rel unit
  dir="$out/traces/$label"; raw="$dir/trace.out"; json="$dir/trace.json"; dot="$dir/trace.dot"; raw_rel="traces/$label/trace.out"
  stage_notice "trace $label / $lemma"
  mkdir -p "$dir"
  print_command "executed-trace[$label]" "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "$TAMARIN_CMD"     --derivcheck-timeout=0 "--prove=$lemma" "--output-json=$json" "--output-dot=$dot" "$ROOT_DIR/$model_rel" >> "$out/commands.txt"
  run_limited_tamarin_command "$out" "$label" "$lemma" "$raw"     "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "$TAMARIN_CMD" --derivcheck-timeout=0 "--prove=$lemma"     "--output-json=$json" "--output-dot=$dot" "$ROOT_DIR/$model_rel" || exit_code=$?
  if [[ "$model_rel" == "$COMBINED_REPLAY_REL" ]]; then suite=combined-replay; else suite=combined-impact; fi
  digest="$(awk -F '\t' -v s="$suite" -v t="$lemma" '$1==s&&$2==t{print $3; exit}' "$out/formula-bodies.tsv")"
  if validate_trace_artifacts "$label" "$ROOT_DIR/$model_rel" "$lemma" "$raw" "$json" "$dot" "$exit_code" "$digest"; then result=PASS; fi
  unit="$(unit_safe_name "$label" "$lemma")"
  append_resource_event "$out" "$suite" "$lemma" "$(classify_target_event "$exit_code" "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS")"     "$exit_code" "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS" "$raw_rel" "$unit"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$label" "$model_rel" "$lemma" "$exit_code" "$result" \
    "traces/$label/trace.out" "traces/$label/trace.json" "traces/$label/trace.dot" >> "$out/trace-aggregate.tsv"
  [[ "$result" == PASS ]]
}

validate_trace_aggregate_structure() {
  local file="$1" expected actual
  [[ -f "$file" ]] || { echo "error: missing trace aggregate: $file" >&2; return 1; }
  [[ "$(head -n1 "$file")" == $'label\tmodel\tlemma\texit_status\tvalidation\traw\tjson\tdot' ]] || {
    echo "error: trace aggregate header mismatch" >&2; return 1; }
  [[ "$(awk -F '\t' 'NR>1 {if(NF!=8 || ($5!="PASS" && $5!="FAIL")) bad=1; n++} END{if(bad) exit 1; print n+0}' "$file")" == 5 ]] || {
    echo "error: trace aggregate must contain exactly five well-formed rows" >&2; return 1; }
  expected=$'duplicate\ttamarin/replay/kwaay_replay_hmac_dedup.spthy\tduplicate_same_base_different_tag_fail_exists\ttraces/duplicate/trace.out\ttraces/duplicate/trace.json\ttraces/duplicate/trace.dot\nnormal-replay\ttamarin/replay/kwaay_replay_hmac_dedup.spthy\tnormal_two_distinct_valid_confirmed_accepts_complete\ttraces/normal-replay/trace.out\ttraces/normal-replay/trace.json\ttraces/normal-replay/trace.dot\nslot1-mismatch\ttamarin/replay/kwaay_replay_hmac_dedup.spthy\thmac_failure_slot1_exists\ttraces/slot1-mismatch/trace.out\ttraces/slot1-mismatch/trace.json\ttraces/slot1-mismatch/trace.dot\nslot2-mismatch\ttamarin/impact/kwaay_impact_hmac_dedup.spthy\thmac_failure_slot2_after_prior_accept_exists\ttraces/slot2-mismatch/trace.out\ttraces/slot2-mismatch/trace.json\ttraces/slot2-mismatch/trace.dot\nnormal-consumer\ttamarin/impact/kwaay_impact_hmac_dedup.spthy\tnormal_two_distinct_valid_confirmed_outputs_consumer_complete\ttraces/normal-consumer/trace.out\ttraces/normal-consumer/trace.json\ttraces/normal-consumer/trace.dot'
  actual="$(awk -F '\t' 'NR>1 {print $1 "\t" $2 "\t" $3 "\t" $6 "\t" $7 "\t" $8}' "$file")"
  [[ "$actual" == "$expected" ]] || {
    echo "error: trace aggregate witness mapping mismatch" >&2; return 1; }
}

validate_trace_all_pass() {
  validate_trace_aggregate_structure "$1" || return 1
  awk -F '\t' 'NR>1 && ($4!=0 || $5!="PASS") {exit 1}' "$1"
}

tamarin_parse_output_is_wellformed() {
  local raw="$1"
  [[ -s "$raw" ]] || return 1
  if LC_ALL=C grep -Eiq \
      'conversion[[:space:]]+to[[:space:]]+guarded[[:space:]]+formula[[:space:]]+failed|unguarded[[:space:]]+variable|well[ -]?formedness[^[:cntrl:]]*(fail|error)|(fail|error)[^[:cntrl:]]*well[ -]?formedness' \
      "$raw"; then
    return 1
  fi
}

validate_parse_validation() {
  local run="$1" file="$run/parse-validation.tsv" expected actual raw
  [[ -f "$file" ]] || { echo "error: missing parse-validation.tsv" >&2; return 1; }
  [[ "$(head -n1 "$file")" == $'model\texit_status\traw_output' ]] || {
    echo "error: parse validation header mismatch" >&2; return 1; }
  [[ "$(awk -F '\t' 'NR>1 {if(NF!=3 || $2!=0) bad=1; n++} END{if(bad) exit 1; print n+0}' "$file")" == 2 ]] || {
    echo "error: parse validation must have exactly two exit-0 rows" >&2; return 1; }
  expected=$'combined-replay\tparse/combined-replay.out\ncombined-impact\tparse/combined-impact.out'
  actual="$(awk -F '\t' 'NR>1 {print $1 "\t" $3}' "$file")"
  [[ "$actual" == "$expected" ]] || { echo "error: parse validation model/path mapping mismatch" >&2; return 1; }
  while IFS=$'\t' read -r _ _ raw; do
    [[ "$raw" == raw_output ]] && continue
    [[ -s "$run/$raw" ]] || { echo "error: missing or empty parse output: $raw" >&2; return 1; }
    tamarin_parse_output_is_wellformed "$run/$raw" || {
      echo "error: Tamarin parse output contains a guarded-formula or wellformedness failure: $raw" >&2
      return 1
    }
  done < "$file"
}

lookup_recorded_formula_digest() {
  local table="$1" suite="$2" lemma="$3" count digest
  count="$(awk -F '\t' -v s="$suite" -v t="$lemma" 'NR>1&&$1==s&&$2==t{n++} END{print n+0}' "$table")"
  [[ "$count" -eq 1 ]] || return 1
  digest="$(awk -F '\t' -v s="$suite" -v t="$lemma" 'NR>1&&$1==s&&$2==t{print $3}' "$table")"
  [[ "$digest" =~ ^[0-9a-f]{64}$ ]] || return 1
  printf '%s\n' "$digest"
}

revalidate_source_trace_artifacts() {
  local run="$1" label model_rel lemma exit_code validation raw json dot suite digest failures=0
  while IFS=$'\t' read -r label model_rel lemma exit_code validation raw json dot; do
    [[ "$label" == label ]] && continue
    if [[ "$model_rel" == "$COMBINED_REPLAY_REL" ]]; then suite=combined-replay
    elif [[ "$model_rel" == "$COMBINED_IMPACT_REL" ]]; then suite=combined-impact
    else failures=1; continue
    fi
    digest="$(lookup_recorded_formula_digest "$run/formula-bodies.tsv" "$suite" "$lemma" || true)"
    [[ -n "$digest" ]] || { failures=1; continue; }
    validate_trace_artifacts "$label" "$ROOT_DIR/$model_rel" "$lemma" "$run/$raw" "$run/$json" "$run/$dot" \
      "$exit_code" "$digest" || failures=1
  done < "$run/trace-aggregate.tsv"
  [[ "$failures" -eq 0 ]]
}

require_summary_value() {
  local file="$1" key="$2" expected="$3" count actual
  count="$(awk -F= -v k="$key" '$1==k{n++} END{print n+0}' "$file")"
  [[ "$count" -eq 1 ]] || { echo "error: summary key count is not one: $key" >&2; return 1; }
  actual="$(awk -F= -v k="$key" '$1==k{print substr($0,index($0,"=")+1)}' "$file")"
  [[ "$actual" == "$expected" ]] || { echo "error: summary mismatch for $key: $actual != $expected" >&2; return 1; }
}

validate_summary_consistency() {
  local run="$1" aggregate="$run/aggregate.tsv" parse="$run/parse-validation.tsv" traces="$run/trace-aggregate.tsv"
  local invoked terminal nonterminal mismatch parse_failures trace_total trace_failures
  [[ -f "$run/summary.txt" ]] || { echo "error: missing source summary" >&2; return 1; }
  invoked="$(awk -F '\t' 'NR>1{n++} END{print n+0}' "$aggregate")"
  terminal="$(awk -F '\t' 'NR>1&&($3=="verified"||$3=="falsified"||$3=="MATCH"){n++} END{print n+0}' "$aggregate")"
  nonterminal="$(awk -F '\t' 'NR>1&&$3=="nonterminal"{n++} END{print n+0}' "$aggregate")"
  mismatch="$(awk -F '\t' 'NR>1&&$3!=$4{n++} END{print n+0}' "$aggregate")"
  parse_failures="$(awk -F '\t' 'NR>1&&$2!=0{n++} END{print n+0}' "$parse")"
  trace_total="$(awk -F '\t' 'NR>1{n++} END{print n+0}' "$traces")"
  trace_failures="$(awk -F '\t' 'NR>1&&$5!="PASS"{n++} END{print n+0}' "$traces")"
  require_summary_value "$run/summary.txt" invoked "$invoked" || return 1
  require_summary_value "$run/summary.txt" terminal "$terminal" || return 1
  require_summary_value "$run/summary.txt" nonterminal "$nonterminal" || return 1
  require_summary_value "$run/summary.txt" mismatch "$mismatch" || return 1
  require_summary_value "$run/summary.txt" parse_failures "$parse_failures" || return 1
  require_summary_value "$run/summary.txt" trace_total "$trace_total" || return 1
  require_summary_value "$run/summary.txt" trace_failures "$trace_failures" || return 1
  require_summary_value "$run/summary.txt" invoked 301 || return 1
  require_summary_value "$run/summary.txt" parse_failures 0 || return 1
  require_summary_value "$run/summary.txt" trace_total 5 || return 1
  require_summary_value "$run/summary.txt" trace_failures 0 || return 1
  require_summary_value "$run/summary.txt" structural_failures 0
}

validate_source_qualification() {
  local run="$1"
  [[ -f "$run/provenance.txt" && -f "$run/formula-bodies.tsv" ]] || {
    echo "error: incomplete source-run metadata: $run" >&2; return 1; }
  validate_source_matrix "$run/aggregate.tsv" || return 1
  validate_parse_validation "$run" || return 1
  validate_trace_all_pass "$run/trace-aggregate.tsv" || return 1
  revalidate_source_trace_artifacts "$run" || return 1
  validate_summary_consistency "$run" || return 1
  [[ -f "$run/source-run-status.txt" && "$(cat "$run/source-run-status.txt")" == VALID ]] || {
    echo "error: source run is not marked VALID: $run" >&2; return 1; }
}

validate_source_run() {
  local run="$1"
  validate_manifest "$run" || return 1
  validate_binding_against_current "$run" || return 1
  validate_source_qualification "$run"
}

source_run() {
  local n="$1" out parse_errors=0 trace_errors=0 structural_errors=0 status parse_exit
  [[ "$n" == 1 || "$n" == 2 ]] || { echo "error: source run must be 1 or 2" >&2; exit 2; }
  if [[ "$n" == 1 ]]; then
    [[ ! -e "$LOG_DIR" ]] || { echo "error: Run 1 requires the entire log directory to be absent: $LOG_DIR" >&2; exit 2; }
  else
    validate_log_top_level run2 || exit 2
    validate_source_run "$LOG_DIR/source-run1" || exit 2
    source_has_nonterminal "$LOG_DIR/source-run1/aggregate.tsv" || {
      echo "error: Run 2 is forbidden unless Run 1 contains at least one nonterminal target" >&2; exit 2; }
  fi
  verify_current_binding_state || exit 2
  static_checks
  resolve_formal_tools || exit 2
  require_resource_isolation || exit 2
  SOURCE_PROGRESS_CURRENT=0
  out="$LOG_DIR/source-run$n"
  [[ ! -e "$out" ]] || { echo "error: source run exists: $out" >&2; exit 2; }
  mkdir -p "$out/parse"
  RUN_STATE_FILE="$out/run-state.txt"
  CURRENT_TARGET_FILE="$out/current-target.txt"
  write_run_state RUNNING "source_run_number=$n" "progress=0/$SOURCE_PROGRESS_TOTAL" \
    "sigkill_note=SIGKILL and whole-WSL OOM shutdown cannot be trapped; per-target cgroup isolation is the primary protection"
  trap 'handle_source_interrupt TERM 143' TERM
  trap 'handle_source_interrupt INT 130' INT
  trap 'handle_source_interrupt HUP 129' HUP
  printf '%s\n' "$AGGREGATE_HEADER" > "$out/aggregate.tsv"
  printf '%s\n' "$RESOURCE_EVENTS_HEADER" > "$out/resource-events.tsv"
  printf 'suite\ttarget\tformula_body_sha256\n' > "$out/formula-bodies.tsv"
  printf 'label\tmodel\tlemma\texit_status\tvalidation\traw\tjson\tdot\n' > "$out/trace-aggregate.tsv"
  : > "$out/commands.txt"
  emit_canonical_matrix > "$out/canonical-target-matrix.tsv"
  write_binding "$out/binding.tsv"
  write_provenance "$out" "$n"
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
  printf 'model\texit_status\traw_output\n' > "$out/parse-validation.tsv"
  stage_notice "parse combined-replay and combined-impact"
  for status in combined-replay combined-impact; do
    local model
    if [[ "$status" == combined-replay ]]; then model="$ROOT_DIR/$COMBINED_REPLAY_REL"; else model="$ROOT_DIR/$COMBINED_IMPACT_REL"; fi
    parse_exit=0
    print_command "executed-parse[$status]" "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "$TAMARIN_CMD" --parse-only "$model" >> "$out/commands.txt"
    "$TIMEOUT_CMD" "$PROOF_TIMEOUT_SECONDS" "$TAMARIN_CMD" --parse-only "$model" > "$out/parse/$status.out" 2>&1 || parse_exit=$?
    if [[ "$parse_exit" -ne 0 ]] || ! tamarin_parse_output_is_wellformed "$out/parse/$status.out"; then
      parse_errors=$((parse_errors+1))
    fi
    printf '%s\t%s\t%s\n' "$status" "$parse_exit" "parse/$status.out" >> "$out/parse-validation.tsv"
  done
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
  if [[ "$SOURCE_PROGRESS_CURRENT" -ne "$SOURCE_PROGRESS_TOTAL" ]]; then
    echo "error: progress counter ended at $SOURCE_PROGRESS_CURRENT, expected $SOURCE_PROGRESS_TOTAL" >&2
    structural_errors=$((structural_errors+1))
  fi
  run_trace "$out" duplicate "$COMBINED_REPLAY_REL" duplicate_same_base_different_tag_fail_exists || trace_errors=$((trace_errors+1))
  run_trace "$out" normal-replay "$COMBINED_REPLAY_REL" normal_two_distinct_valid_confirmed_accepts_complete || trace_errors=$((trace_errors+1))
  run_trace "$out" slot1-mismatch "$COMBINED_REPLAY_REL" hmac_failure_slot1_exists || trace_errors=$((trace_errors+1))
  run_trace "$out" slot2-mismatch "$COMBINED_IMPACT_REL" hmac_failure_slot2_after_prior_accept_exists || trace_errors=$((trace_errors+1))
  run_trace "$out" normal-consumer "$COMBINED_IMPACT_REL" normal_two_distinct_valid_confirmed_outputs_consumer_complete || trace_errors=$((trace_errors+1))
  rm -f "$CURRENT_TARGET_FILE"
  validate_trace_aggregate_structure "$out/trace-aggregate.tsv" || structural_errors=$((structural_errors+1))
  validate_source_matrix "$out/aggregate.tsv" || structural_errors=$((structural_errors+1))
  verify_repo_clean_except_logs || structural_errors=$((structural_errors+1))
  awk -F '\t' -v pe="$parse_errors" -v te="$trace_errors" -v se="$structural_errors" '
    NR>1 {n++; if($3=="verified"||$3=="falsified"||$3=="MATCH") t++; if($3!=$4)m++; if($3=="nonterminal") nt++}
    END{printf "invoked=%d\nterminal=%d\nnonterminal=%d\nmismatch=%d\nparse_failures=%d\ntrace_total=5\ntrace_failures=%d\nstructural_failures=%d\n",n,t,nt,m,pe,te,se}' \
    "$out/aggregate.tsv" > "$out/summary.txt"
  local final_status=INVALID manifest_ok=0
  if [[ "$parse_errors" -eq 0 && "$trace_errors" -eq 0 && "$structural_errors" -eq 0 ]]; then
    final_status=VALID
    printf '%s\n' VALID > "$out/source-run-status.txt"
    write_run_state COMPLETE "source_run_number=$n" "final_status=VALID" "progress=$SOURCE_PROGRESS_CURRENT/$SOURCE_PROGRESS_TOTAL"
  else
    printf '%s\n' INVALID > "$out/source-run-status.txt"
    write_run_state COMPLETE_INVALID "source_run_number=$n" "final_status=INVALID"
  fi
  trap - TERM INT HUP
  stage_notice "source-run$n final manifest"
  if make_manifest "$out"; then manifest_ok=1; fi
  if [[ "$final_status" == VALID ]]; then
    if [[ "$manifest_ok" -ne 1 ]] || ! validate_source_qualification "$out" || ! validate_manifest "$out"; then
      final_status=INVALID
      printf '%s\n' INVALID > "$out/source-run-status.txt"
      write_run_state COMPLETE_INVALID "source_run_number=$n" "final_status=INVALID"
      stage_notice "source-run$n manifest (INVALID recovery)"
      make_manifest "$out" >/dev/null 2>&1 || true
    fi
  fi
  if [[ "$final_status" == VALID ]]; then
    echo "source_run$n=VALID_COMPLETE_INVOCATION"
    return 0
  fi
  echo "source_run$n=INVALID_COMPLETE_INVOCATION"
  return 1
}

lookup_actual() { awk -F '\t' -v s="$2" -v t="$3" 'NR>1 && $1==s && $2==t {print $3; exit}' "$1"; }

select_composite() {
  local run1="$1" run2="$2" selection="$3" vector="$4" summary="$5"
  local suite target expected r1 r2 selected chosen reason match
  local unresolved=0 mismatch=0 conflicts=0
  printf 'suite\ttarget\texpected\trun1\trun2\tselected_run\tselected_status\treason\n' > "$selection"
  printf 'suite\ttarget\tactual_status\texpected_status\tselected_run\tmatch\n' > "$vector"
  while IFS=$'\t' read -r suite target expected; do
    [[ "$suite" == suite ]] && continue
    r1="$(lookup_actual "$run1" "$suite" "$target")"; r2=missing
    [[ -z "$run2" ]] || r2="$(lookup_actual "$run2" "$suite" "$target")"
    [[ -n "$r2" ]] || r2=missing
    selected=none; chosen=nonterminal; reason="Run 1 nonterminal and no legal terminal fallback"
    if terminal_status "$r1"; then
      selected=run1; chosen="$r1"; reason="Run 1 primary terminal"
      if terminal_status "$r2" && [[ "$r1" != "$r2" ]]; then conflicts=$((conflicts+1)); fi
    elif terminal_status "$r2"; then
      selected=run2; chosen="$r2"; reason="Run 1 nonterminal; Run 2 terminal fallback"
    else
      unresolved=$((unresolved+1))
    fi
    if [[ "$chosen" == "$expected" ]]; then match=MATCH; else match=MISMATCH; mismatch=$((mismatch+1)); fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$expected" "$r1" "$r2" "$selected" "$chosen" "$reason" >> "$selection"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$suite" "$target" "$chosen" "$expected" "$selected" "$match" >> "$vector"
  done < <(emit_canonical_matrix)
  {
    echo "classification=transparent composite; canonical 301-target matrix; Run 1 primary"
    echo "terminal_conflicts=$conflicts"
    echo "unresolved=$unresolved"
    echo "mismatches=$mismatch"
  } > "$summary"
  [[ "$conflicts" -eq 0 && "$unresolved" -eq 0 && "$mismatch" -eq 0 ]]
}

assemble_composite() {
  local run1="$LOG_DIR/source-run1" run2="$LOG_DIR/source-run2" run2_aggregate=
  stage_notice "composite validation and selection"
  validate_log_top_level assemble || exit 2
  verify_current_binding_state || exit 2
  static_checks
  validate_source_run "$run1" || exit 2
  if [[ -d "$run2" ]]; then
    validate_source_run "$run2" || exit 2
    source_has_nonterminal "$run1/aggregate.tsv" || { echo "error: a Run 2 exists although Run 1 has no nonterminal target" >&2; exit 2; }
    cmp -s "$run1/binding.tsv" "$run2/binding.tsv" || { echo "error: Run 1/Run 2 binding conflict" >&2; exit 2; }
    run2_aggregate="$run2/aggregate.tsv"
  fi
  select_composite "$run1/aggregate.tsv" "$run2_aggregate" "$LOG_DIR/composite-selection.tsv" \
    "$LOG_DIR/composite-result-vector.tsv" "$LOG_DIR/composite-summary.txt" || {
      echo "error: composite has unresolved, mismatch, or terminal conflict" >&2; exit 1; }
  verify_repo_clean_except_logs || exit 2
  stage_notice "composite manifest"
  make_manifest "$LOG_DIR"
  echo "composite=PASS"
}

write_synthetic_aggregate() {
  local destination="$1" override_suite="${2:-}" override_target="${3:-}" override_status="${4:-}"
  printf '%s\n' "$AGGREGATE_HEADER" > "$destination"
  while IFS=$'\t' read -r suite target expected; do
    [[ "$suite" == suite ]] && continue
    local actual="$expected"
    if [[ "$suite" == "$override_suite" && "$target" == "$override_target" ]]; then actual="$override_status"; fi
    printf '%s\t%s\t%s\t%s\t0\tfalse\tsynthetic/%s/%s.out\n' "$suite" "$target" "$actual" "$expected" "$suite" "$target" >> "$destination"
  done < <(emit_canonical_matrix)
}

write_synthetic_trace_dot() {
  local label="$1" destination="$2" events
  case "$label" in
    duplicate) events='DuplicateDetected(B,b,r,i1,A,i2,A,m) BatchFail(B,b,r) BatchClosed(B,b,r) ConsumeReceiverState(B,r)' ;;
    normal-replay) events='ConfirmedSend(A1,B,m1,s1,k1,t1) ConfirmedSend(A2,B,m2,s2,k2,t2) DedupPassed(B,b,r,i1,A1,m1,i2,A2,m2) HmacValidated(B,A1,b,i1,r,m1,s1,k1,t1) HmacValidated(B,A2,b,i2,r,m2,s2,k2,t2) ConfirmedReceiverAccept(B,A1,b,i1,r,m1,s1,k1,t1) ConfirmedReceiverAccept(B,A2,b,i2,r,m2,s2,k2,t2) BatchComplete(B,b,r)' ;;
    slot1-mismatch) events='HmacValidationFailed(B,A1,b,i1,r,m1,s1,k1,bad,t1) BatchFail(B,b,r)' ;;
    slot2-mismatch) events='ConfirmedReceiverAccept(B,A1,b,i1,r,m1,s1,k1,t1) HmacValidationFailed(B,A2,b,i2,r,m2,s2,k2,bad,t2) BatchFail(B,b,r)' ;;
    normal-consumer) events='AcceptOutputCreated(aid1,B,A1,b,i1,r,m1,s1,k1) AcceptOutputCreated(aid2,B,A2,b,i2,r,m2,s2,k2) InstallFromAccept(aid1,B,h1,A1,b,i1,r,m1,s1,k1) InstallFromAccept(aid2,B,h2,A2,b,i2,r,m2,s2,k2) ConsumerComplete(B,b,r)' ;;
    *) return 1 ;;
  esac
  printf 'digraph trace { node [label="%s"]; }\n' "$events" > "$destination"
}

write_synthetic_qualified_source() {
  local run="$1" label model_rel lemma suite theory digest dir
  mkdir -p "$run/parse"
  write_synthetic_aggregate "$run/aggregate.tsv"
  printf 'model\texit_status\traw_output\ncombined-replay\t0\tparse/combined-replay.out\ncombined-impact\t0\tparse/combined-impact.out\n' > "$run/parse-validation.tsv"
  printf 'synthetic parse success\n' > "$run/parse/combined-replay.out"
  printf 'synthetic parse success\n' > "$run/parse/combined-impact.out"
  printf 'suite\ttarget\tformula_body_sha256\n' > "$run/formula-bodies.tsv"
  printf 'label\tmodel\tlemma\texit_status\tvalidation\traw\tjson\tdot\n' > "$run/trace-aggregate.tsv"
  while IFS=$'\t' read -r label model_rel lemma; do
    case "$label" in
      duplicate|normal-replay|slot1-mismatch) suite=combined-replay ;;
      *) suite=combined-impact ;;
    esac
    theory="$(awk '/^theory[[:space:]]+/{print $2; exit}' "$ROOT_DIR/$model_rel")"
    digest="$(formula_digest_for "$ROOT_DIR/$model_rel" "$lemma")"
    printf '%s\t%s\t%s\n' "$suite" "$lemma" "$digest" >> "$run/formula-bodies.tsv"
    dir="$run/traces/$label"; mkdir -p "$dir"
    printf '[Theory %s]\n  %s (exists-trace): verified (1 steps)\n' "$theory" "$lemma" > "$dir/trace.out"
    printf '{"graphs":[{}],"theory":"%s","lemma":"%s"}\n' "$theory" "$lemma" > "$dir/trace.json"
    write_synthetic_trace_dot "$label" "$dir/trace.dot"
    printf '%s\t%s\t%s\t0\tPASS\ttraces/%s/trace.out\ttraces/%s/trace.json\ttraces/%s/trace.dot\n' \
      "$label" "$model_rel" "$lemma" "$label" "$label" "$label" >> "$run/trace-aggregate.tsv"
  done <<EOF
duplicate	$COMBINED_REPLAY_REL	duplicate_same_base_different_tag_fail_exists
normal-replay	$COMBINED_REPLAY_REL	normal_two_distinct_valid_confirmed_accepts_complete
slot1-mismatch	$COMBINED_REPLAY_REL	hmac_failure_slot1_exists
slot2-mismatch	$COMBINED_IMPACT_REL	hmac_failure_slot2_after_prior_accept_exists
normal-consumer	$COMBINED_IMPACT_REL	normal_two_distinct_valid_confirmed_outputs_consumer_complete
EOF
  printf 'synthetic provenance\n' > "$run/provenance.txt"
  printf 'invoked=301\nterminal=301\nnonterminal=0\nmismatch=0\nparse_failures=0\ntrace_total=5\ntrace_failures=0\nstructural_failures=0\n' > "$run/summary.txt"
  printf 'VALID\n' > "$run/source-run-status.txt"
}

expect_validator_failure() { if "$@" >/dev/null 2>&1; then echo "error: negative test unexpectedly passed: $*" >&2; return 1; fi; }

self_test() {
  local tmp base fixture selection vector summary before_log_exists=0 failures=0 mock classification pv_actual pv_expected synthetic_run
  local probe_out resource_out timeout_cmd resource_exit next_exit event old_memory old_run_state old_current_target old_started old_unit old_wait old_suite old_target old_raw interrupt_dir unit active_state signal_status status
  [[ -e "$LOG_DIR" ]] && before_log_exists=1
  static_checks >/dev/null || failures=1
  tmp="$(mktemp -d)"; base="$tmp/base.tsv"
  if ! unexpected_git_status > "$tmp/unexpected-git-status.out"; then failures=1; fi
  if grep -Fq "$LOG_REL" "$tmp/unexpected-git-status.out"; then failures=1; fi
  write_synthetic_aggregate "$base"
  validate_source_matrix "$base" || failures=1

  fixture="$tmp/missing.tsv"; awk 'NR!=2' "$base" > "$fixture"; expect_validator_failure validate_source_matrix "$fixture" || failures=1
  fixture="$tmp/duplicate.tsv"; cp "$base" "$fixture"; sed -n '2p' "$base" >> "$fixture"; expect_validator_failure validate_source_matrix "$fixture" || failures=1
  fixture="$tmp/extra.tsv"; cp "$base" "$fixture"; printf 'extra\ttarget\tverified\tverified\t0\tfalse\tx\n' >> "$fixture"; expect_validator_failure validate_source_matrix "$fixture" || failures=1
  fixture="$tmp/expected.tsv"; awk -F '\t' 'BEGIN{OFS="\t"} NR==2{$4=($4=="verified"?"falsified":"verified")} {print}' "$base" > "$fixture"; expect_validator_failure validate_source_matrix "$fixture" || failures=1
  fixture="$tmp/header.tsv"; { echo 'wrong-header'; tail -n +2 "$base"; } > "$fixture"; expect_validator_failure validate_source_matrix "$fixture" || failures=1

  mkdir -p "$tmp/manifest"; printf 'alpha\n' > "$tmp/manifest/a"; make_manifest "$tmp/manifest" >/dev/null || failures=1
  printf 'tamper\n' >> "$tmp/manifest/a"; expect_validator_failure validate_manifest "$tmp/manifest" || failures=1
  make_manifest "$tmp/manifest" >/dev/null || failures=1; printf 'extra\n' > "$tmp/manifest/extra"; expect_validator_failure validate_manifest "$tmp/manifest" || failures=1
  make_manifest "$tmp/manifest" >/dev/null || failures=1; rm -f "$tmp/manifest/a"; expect_validator_failure validate_manifest "$tmp/manifest" || failures=1
  mkdir -p "$tmp/final-manifest"
  printf '%s\n' payload > "$tmp/final-manifest/payload.txt"
  printf '%s\n' VALID > "$tmp/final-manifest/source-run-status.txt"
  printf '%s\n' COMPLETE > "$tmp/final-manifest/run-state.txt"
  make_manifest "$tmp/final-manifest" >/dev/null || failures=1
  validate_manifest "$tmp/final-manifest" || failures=1

  selection="$tmp/selection.tsv"; vector="$tmp/vector.tsv"; summary="$tmp/summary.txt"
  select_composite "$base" "" "$selection" "$vector" "$summary" || failures=1
  write_synthetic_aggregate "$tmp/run1-nonterminal.tsv" combined-replay normal_confirmed_single_accept nonterminal
  write_synthetic_aggregate "$tmp/run2.tsv"
  expect_validator_failure select_composite "$tmp/run1-nonterminal.tsv" "" "$selection" "$vector" "$summary" || failures=1
  select_composite "$tmp/run1-nonterminal.tsv" "$tmp/run2.tsv" "$selection" "$vector" "$summary" || failures=1
  grep -Fq $'combined-replay\tnormal_confirmed_single_accept\tverified\tnonterminal\tverified\trun2' "$selection" || failures=1
  write_synthetic_aggregate "$tmp/run1-unexpected.tsv" combined-replay normal_confirmed_single_accept falsified
  if source_has_nonterminal "$tmp/run1-unexpected.tsv"; then failures=1; fi
  expect_validator_failure select_composite "$tmp/run1-unexpected.tsv" "$tmp/run2.tsv" "$selection" "$vector" "$summary" || failures=1
  grep -Fq $'combined-replay\tnormal_confirmed_single_accept\tverified\tfalsified\tverified\trun1' "$selection" || failures=1

  : > "$tmp/empty.out"; classification="$(parse_tamarin_result target "$tmp/empty.out" 0)"; [[ "$classification" == nonterminal ]] || failures=1
  printf '<<loop>>\n' > "$tmp/loop.out"; classification="$(parse_tamarin_result target "$tmp/loop.out" 0)"; [[ "$classification" == nonterminal ]] || failures=1
  printf 'unknown result\n' > "$tmp/unknown.out"; classification="$(parse_tamarin_result target "$tmp/unknown.out" 0)"; [[ "$classification" == nonterminal ]] || failures=1
  printf '  target (exists-trace): verified (1 steps)\n' > "$tmp/timeout.out"; classification="$(parse_tamarin_result target "$tmp/timeout.out" 124)"; [[ "$classification" == nonterminal ]] || failures=1
  printf '  target (exists-trace): verified (1 steps)\n' > "$tmp/verified.out"
  classification="$(parse_tamarin_result target "$tmp/verified.out" 1)"; [[ "$classification" == nonterminal ]] || failures=1
  classification="$(parse_tamarin_result target "$tmp/verified.out" 0)"; [[ "$classification" == verified ]] || failures=1
  printf '  target (exists-trace): falsified - found trace (2 steps)\n' > "$tmp/falsified.out"
  classification="$(parse_tamarin_result target "$tmp/falsified.out" 2)"; [[ "$classification" == nonterminal ]] || failures=1
  classification="$(parse_tamarin_result target "$tmp/falsified.out" 0)"; [[ "$classification" == falsified ]] || failures=1
  { cat "$tmp/verified.out"; cat "$tmp/verified.out"; } > "$tmp/duplicate-result.out"
  classification="$(parse_tamarin_result target "$tmp/duplicate-result.out" 0)"; [[ "$classification" == nonterminal ]] || failures=1

  pv_expected="$tmp/pv-expected"; pv_actual="$tmp/pv-actual"
  printf 'RESULT first\nRESULT second\n' > "$pv_expected"; cp "$pv_expected" "$pv_actual"
  compare_proverif_results "$pv_actual" "$pv_expected" 0 0 || failures=1
  printf 'RESULT second\nRESULT first\n' > "$pv_actual"; expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 0 0 || failures=1
  printf 'RESULT first\n' > "$pv_actual"; expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 0 0 || failures=1
  printf 'RESULT first\nRESULT second\nRESULT third\n' > "$pv_actual"; expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 0 0 || failures=1
  : > "$pv_actual"; expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 0 0 || failures=1
  cp "$pv_expected" "$pv_actual"; expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 1 0 || failures=1
  expect_validator_failure compare_proverif_results "$pv_actual" "$pv_expected" 0 1 || failures=1

  printf '{"graphs":[{}]}\n' > "$tmp/valid.json"; validate_json_trace "$tmp/valid.json" || failures=1
  printf '{invalid\n' > "$tmp/invalid.json"; expect_validator_failure validate_json_trace "$tmp/invalid.json" || failures=1
  printf '{"graphs":[]}\n' > "$tmp/empty-graphs.json"; expect_validator_failure validate_json_trace "$tmp/empty-graphs.json" || failures=1
  printf 'digraph G { a -> b; }\n' > "$tmp/valid.dot"; validate_dot_digraph "$tmp/valid.dot" || failures=1
  printf 'graph G { a -- b;\n' > "$tmp/invalid.dot"; expect_validator_failure validate_dot_digraph "$tmp/invalid.dot" || failures=1
  printf '[Theory CorrectTheory]\n' > "$tmp/theory-bracket.out"; trace_raw_matches_theory "$tmp/theory-bracket.out" CorrectTheory || failures=1
  printf 'theory CorrectTheory\n' > "$tmp/theory-source.out"; trace_raw_matches_theory "$tmp/theory-source.out" CorrectTheory || failures=1
  printf '  theory CorrectTheory  \r\n' > "$tmp/theory-crlf.out"; trace_raw_matches_theory "$tmp/theory-crlf.out" CorrectTheory || failures=1
  printf 'theory WrongTheory\n' > "$tmp/theory-wrong.out"; expect_validator_failure trace_raw_matches_theory "$tmp/theory-wrong.out" CorrectTheory || failures=1
  printf 'theory CorrectTheory_extra\n' > "$tmp/theory-extra.out"; expect_validator_failure trace_raw_matches_theory "$tmp/theory-extra.out" CorrectTheory || failures=1
  printf 'ordinary log mentions CorrectTheory but has no marker\n' > "$tmp/theory-missing.out"; expect_validator_failure trace_raw_matches_theory "$tmp/theory-missing.out" CorrectTheory || failures=1

  printf '/* All wellformedness checks were successful. */\n' > "$tmp/wellformed.out"
  tamarin_parse_output_is_wellformed "$tmp/wellformed.out" || failures=1
  printf 'conversion to guarded formula failed: unguarded variable(s) tag2\n' > "$tmp/guarded-failure.out"
  expect_validator_failure tamarin_parse_output_is_wellformed "$tmp/guarded-failure.out" || failures=1
  printf 'Wellformedness check failed\n' > "$tmp/wellformedness-failed.out"
  expect_validator_failure tamarin_parse_output_is_wellformed "$tmp/wellformedness-failed.out" || failures=1
  printf 'ERROR: protocol well-formedness failure\n' > "$tmp/wellformedness-error.out"
  expect_validator_failure tamarin_parse_output_is_wellformed "$tmp/wellformedness-error.out" || failures=1

  synthetic_run="$tmp/source-run"
  write_synthetic_qualified_source "$synthetic_run"
  validate_source_qualification "$synthetic_run" || failures=1
  printf '%s\n' INVALID > "$synthetic_run/source-run-status.txt"
  expect_validator_failure validate_source_qualification "$synthetic_run" || failures=1
  printf '%s\n' VALID > "$synthetic_run/source-run-status.txt"
  sed -i 's/combined-replay\t0/combined-replay\t1/' "$synthetic_run/parse-validation.tsv"
  expect_validator_failure validate_source_qualification "$synthetic_run" || failures=1
  sed -i 's/combined-replay\t1/combined-replay\t0/' "$synthetic_run/parse-validation.tsv"
  sed -i '0,/\tPASS\t/s//\tFAIL\t/' "$synthetic_run/trace-aggregate.tsv"
  expect_validator_failure validate_source_qualification "$synthetic_run" || failures=1
  sed -i '0,/\tFAIL\t/s//\tPASS\t/' "$synthetic_run/trace-aggregate.tsv"
  sed -i 's/invoked=301/invoked=300/' "$synthetic_run/summary.txt"
  expect_validator_failure validate_source_qualification "$synthetic_run" || failures=1
  sed -i 's/invoked=300/invoked=301/' "$synthetic_run/summary.txt"
  validate_source_qualification "$synthetic_run" || failures=1

  mkdir -p "$tmp/log-layout/source-run1"
  validate_log_top_level_at "$tmp/log-layout" run2 || failures=1
  mkdir -p "$tmp/log-layout/source-run2"
  expect_validator_failure validate_log_top_level_at "$tmp/log-layout" run2 || failures=1
  validate_log_top_level_at "$tmp/log-layout" assemble || failures=1
  printf 'stale\n' > "$tmp/log-layout/composite-summary.txt"
  expect_validator_failure validate_log_top_level_at "$tmp/log-layout" assemble || failures=1

  classification="$(classify_target_event 124 exit-code 1 124)"; [[ "$classification" == timeout ]] || failures=1
  classification="$(classify_target_event 137 oom-kill 2 9)"; [[ "$classification" == oom_kill ]] || failures=1
  classification="$(classify_target_event 137 signal 2 9)"; [[ "$classification" == sigkill ]] || failures=1
  classification="$(classify_target_event 2 exit-code 1 2)"; [[ "$classification" == nonzero_exit ]] || failures=1
  classification="$(classify_target_event 0 success 1 0)"; [[ "$classification" == none ]] || failures=1
  [[ "$(normalize_systemd_exit_status 1 1 124)" == 124 ]] || failures=1
  [[ "$(normalize_systemd_exit_status 1 2 9)" == 137 ]] || failures=1

  mock="$tmp/mock-version"; mkdir -p "$mock"
  printf '#!/usr/bin/env bash\necho "read failed 9: Bad file descriptor" >&2\nexit 1\n' > "$mock/proverif-bad"; chmod +x "$mock/proverif-bad"
  PROVERIF_CMD=("$mock/proverif-bad"); probe_out="$tmp/proverif-bad.probe"; write_proverif_version_probe > "$probe_out"
  grep -Fxq 'proverif_version_probe_result=unavailable' "$probe_out" || failures=1
  grep -Fxq 'proverif_version_probe_bad_fd=true' "$probe_out" || failures=1
  if grep -q '^proverif_version=' "$probe_out"; then failures=1; fi
  printf '#!/usr/bin/env bash\necho "read failed 9: Bad file descriptor" >&2\necho "ProVerif 2.05: synthetic version"\nexit 0\n' > "$mock/proverif-good"; chmod +x "$mock/proverif-good"
  PROVERIF_CMD=("$mock/proverif-good"); probe_out="$tmp/proverif-good.probe"; write_proverif_version_probe > "$probe_out"
  grep -Fxq 'proverif_version=ProVerif 2.05: synthetic version' "$probe_out" || failures=1
  grep -Fxq 'proverif_version_probe_bad_fd=true' "$probe_out" || failures=1

  old_memory="$TAMARIN_MEMORY_MAX_MB"; old_run_state="$RUN_STATE_FILE"; old_current_target="$CURRENT_TARGET_FILE"
  old_started="$CURRENT_STARTED_AT"; old_unit="$CURRENT_SYSTEMD_UNIT"; old_wait="$CURRENT_SYSTEMD_WAIT_PID"
  old_suite="$CURRENT_SUITE"; old_target="$CURRENT_TARGET"; old_raw="$CURRENT_RAW"
  resource_out="$tmp/resource"; mkdir -p "$resource_out"
  printf '%s\n' "$RESOURCE_EVENTS_HEADER" > "$resource_out/resource-events.tsv"
  printf '%s\n' "$AGGREGATE_HEADER" > "$resource_out/aggregate.tsv"
  RUN_STATE_FILE="$resource_out/run-state.txt"; CURRENT_TARGET_FILE="$resource_out/current-target.txt"; CURRENT_STARTED_AT=
  write_run_state RUNNING synthetic=true
  write_current_target running synthetic atomic "$resource_out/atomic.out" 123 unit-test
  grep -Fxq 'phase=running' "$CURRENT_TARGET_FILE" || failures=1
  if find "$resource_out" -maxdepth 1 -name 'current-target.txt.tmp.*' | grep -q .; then failures=1; fi
  timeout_cmd="$(command -v timeout)"
  TAMARIN_MEMORY_MAX_MB=32
  require_resource_isolation || failures=1
  resource_exit=0
  run_limited_tamarin_command "$resource_out" synthetic resource-limit "$resource_out/resource-limit.out" \
    /usr/bin/python3 -c 'a=bytearray(256*1024*1024); print(len(a))' || resource_exit=$?
  event="$(classify_target_event "$resource_exit" "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS")"
  status="$(parse_tamarin_result resource-limit "$resource_out/resource-limit.out" "$resource_exit")"
  [[ "$resource_exit" -ne 0 && "$event" == oom_kill && "$status" == nonterminal ]] || failures=1
  append_resource_event "$resource_out" synthetic resource-limit "$event" "$resource_exit" \
    "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS" resource-limit.out "$CURRENT_SYSTEMD_UNIT"
  next_exit=0
  run_limited_tamarin_command "$resource_out" synthetic after-resource-limit "$resource_out/after-resource-limit.out" /bin/echo after-resource-limit || next_exit=$?
  [[ "$next_exit" -eq 0 ]] || failures=1
  grep -Fxq 'after-resource-limit' "$resource_out/after-resource-limit.out" || failures=1
  TAMARIN_MEMORY_MAX_MB=128
  resource_exit=0
  run_limited_tamarin_command "$resource_out" synthetic timeout-target "$resource_out/timeout-target.out" \
    "$timeout_cmd" 1 /bin/sleep 3 || resource_exit=$?
  event="$(classify_target_event "$resource_exit" "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS")"
  [[ "$resource_exit" -eq 124 && "$event" == timeout ]] || failures=1
  append_resource_event "$resource_out" synthetic timeout-target "$event" "$resource_exit" \
    "$LAST_SYSTEMD_RESULT" "$LAST_EXEC_MAIN_CODE" "$LAST_EXEC_MAIN_STATUS" timeout-target.out "$CURRENT_SYSTEMD_UNIT"
  unit="$(unit_safe_name synthetic term-cleanup)"
  CURRENT_SYSTEMD_UNIT="$unit"; CURRENT_SYSTEMD_WAIT_PID=; CURRENT_SUITE=synthetic; CURRENT_TARGET=term-cleanup; CURRENT_RAW=term-cleanup.out; CURRENT_STARTED_AT="$(iso_timestamp)"
  systemd-run --user --quiet --unit="$unit" --property=KillMode=control-group \
    --property=StandardInput=null --property=StandardOutput=null --property=StandardError=null /bin/sleep 60 >/dev/null || failures=1
  terminate_current_proof TERM
  active_state="$(systemctl --user is-active "$unit.service" 2>/dev/null || true)"
  [[ "$active_state" != active ]] || failures=1
  grep -Fxq 'event=TERM' "$CURRENT_TARGET_FILE" || failures=1
  interrupt_dir="$tmp/interrupted"; mkdir -p "$interrupt_dir"
  printf 'VALID\n' > "$interrupt_dir/source-run-status.txt"
  printf 'synthetic manifest\n' > "$interrupt_dir/SHA256SUMS.txt"
  signal_status=0
  ( RUN_STATE_FILE="$interrupt_dir/run-state.txt"; CURRENT_TARGET_FILE="$interrupt_dir/current-target.txt"; \
    SOURCE_RUN_INTERRUPTING=0; CURRENT_SYSTEMD_UNIT=; CURRENT_SYSTEMD_WAIT_PID=; CURRENT_SUITE=synthetic; \
    CURRENT_TARGET=int-cleanup; CURRENT_RAW=interrupted.out; CURRENT_STARTED_AT="$(iso_timestamp)"; \
    handle_source_interrupt INT 130 ) || signal_status=$?
  [[ "$signal_status" -eq 130 ]] || failures=1
  grep -Fxq 'INTERRUPTED' "$interrupt_dir/run-state.txt" || failures=1
  grep -Fxq 'signal=INT' "$interrupt_dir/run-state.txt" || failures=1
  [[ ! -e "$interrupt_dir/source-run-status.txt" && ! -e "$interrupt_dir/SHA256SUMS.txt" ]] || failures=1
  TAMARIN_MEMORY_MAX_MB="$old_memory"; RUN_STATE_FILE="$old_run_state"; CURRENT_TARGET_FILE="$old_current_target"
  CURRENT_STARTED_AT="$old_started"; CURRENT_SYSTEMD_UNIT="$old_unit"; CURRENT_SYSTEMD_WAIT_PID="$old_wait"
  CURRENT_SUITE="$old_suite"; CURRENT_TARGET="$old_target"; CURRENT_RAW="$old_raw"

  mock="$tmp/mock-bin"; mkdir -p "$mock"
  printf '#!/usr/bin/env bash\nexit 0\n' > "$mock/proverif"; chmod +x "$mock/proverif"
  (PATH="$mock:/usr/bin:/bin"; resolve_proverif; [[ "${PROVERIF_CMD[0]}" == "$mock/proverif" && "$PROVERIF_NEEDS_WIN_PATH" -eq 0 ]]) || failures=1
  rm -f "$mock/proverif"; printf '#!/usr/bin/env bash\nexit 0\n' > "$mock/proverif.exe"; chmod +x "$mock/proverif.exe"
  (PATH="$mock:/usr/bin:/bin"; resolve_proverif; [[ "${PROVERIF_CMD[0]}" == "$mock/proverif.exe" && "$PROVERIF_NEEDS_WIN_PATH" -eq 1 ]]) || failures=1
  [[ "$(readlink -f "$GIT_ROOT_REPORTED")" == "$ROOT_DIR" ]] || failures=1

  rm -rf "$tmp"
  if [[ "$before_log_exists" -eq 0 && -e "$LOG_DIR" ]]; then echo "error: self-test created formal log directory" >&2; failures=1; fi
  [[ "$failures" -eq 0 ]] || return 1
  echo "target_matrix_tests=PASS"
  echo "manifest_tamper_tests=PASS"
  echo "final_manifest_order_test=PASS"
  echo "matrix_missing_duplicate_extra_tests=PASS"
  echo "composite_synthetic_tests=PASS"
  echo "clean_directory_tests=PASS"
  echo "path_tool_resolution_tests=PASS"
  echo "tamarin_terminal_classification_tests=PASS"
  echo "proverif_order_comparator_tests=PASS"
  echo "json_dot_trace_tests=PASS"
  echo "source_run_qualification_tests=PASS"
  echo "gawk_unexpected_git_status_test=PASS"
  echo "parse_output_failure_gate_tests=PASS"
  echo "resource_limit_synthetic_tests=PASS"
  echo "signal_cleanup_tests=PASS"
  echo "proverif_bad_fd_probe_tests=PASS"
  echo "run_state_current_target_tests=PASS"
  echo "self_test=PASS"
}

usage() {
  echo "usage: $RUNNER_REL [--memory-max-mb N] --static-only | --self-test | --source-run 1|2 | --assemble-composite" >&2
  exit 2
}


args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --memory-max-mb)
      [[ $# -ge 2 ]] || usage
      TAMARIN_MEMORY_MAX_MB="$2"
      shift 2
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done
set -- "${args[@]}"
validate_positive_mb "$TAMARIN_MEMORY_MAX_MB" || exit 2

case "${1:-}" in
  --static-only) [[ $# -eq 1 ]] || usage; static_checks ;;
  --self-test) [[ $# -eq 1 ]] || usage; self_test ;;
  --source-run) [[ $# -eq 2 ]] || usage; source_run "$2" ;;
  --assemble-composite) [[ $# -eq 1 ]] || usage; assemble_composite ;;
  *) usage ;;
esac
