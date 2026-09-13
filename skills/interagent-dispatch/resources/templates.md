# Dispatch Templates (Copy-Paste Ready)

This reference contains the standard dispatch contracts for all 4 profiles.

---

## 1. BASIC Profile (Bounded / Read-Only / Tiny Fix)

```markdown
---
protocol: agent-dispatch/v1
profile: BASIC
role: executor
not_role: [orchestrator, approver]
---

# TASK
GOAL: <Observable final capability or state>
DONE WHEN: <Observable check: command output or diff>
TARGET: <Single bounded target>

# SCOPE
Operate exclusively inside:
- path: <allowed_path>

# VERIFICATION
Execute: `<exact_readback_or_diff_command>`

# RETURN CONTRACT
Conclude with this block:
```yaml
result_receipt:
  status: done | blocked | failed
  summary: "<one sentence>"
  modified_files: []
  evidence:
    - command: "<command>"
      exit_code: 0
  residual_risks: []
```
```

---

## 2. CONTROLLED Profile (Standard Dev / Local Tests / Tool Interfacing)

```markdown
---
protocol: agent-dispatch/v1
profile: CONTROLLED
role: executor
not_role: [orchestrator, approver]
---

# TASK
GOAL: <Observable final capability or state>
DONE WHEN: <Observable check: test suite pass + artifacts written>
TARGET: <Single bounded feature or bugfix>

# SCOPE & OWNERSHIP
Operate exclusively on:
- path: <allowed_path_1>
- path: <allowed_path_2>

Ownership check: Fail-closed on dirty files within declared scope; ignore lateral workspace noise.

# FROZEN CONTEXT
- baseline_sha: <commit/hash>
- working_directory: <abs_path>

# EXECUTION GATES
1. PRE-FLIGHT: Verify absolute paths, active branch, and tool availability before mutation.
2. DISCOVERY: Load environment and dependencies; fail-closed if required secrets or env vars are missing.
3. VALIDATION: Execute `<exact_test_command>`. Expected exit code: 0.

# AUTHORITY & HARD STOPS
Authority: Decision belongs exclusively to Orchestrator.
Hard Stop: On unexpected failure, missing dependency, or scope ambiguity → STOP immediately and return `status: blocked`. Escalate directly upon blocker encounter.

# RETURN CONTRACT
Conclude with this block:
```yaml
result_receipt:
  status: done | partial | blocked | failed
  summary: "<one sentence summary>"
  modified_files: [<paths>]
  evidence:
    - command: "<exact test command>"
      exit_code: 0
      test_output_summary: "<key pass/fail stats>"
  residual_risks: []
```
```

---

## 3. GOVERNED Profile (Multi-File / Protected State / Rollback)

```markdown
---
protocol: agent-dispatch/v1
profile: GOVERNED
role: executor
not_role: [orchestrator, approver, release_manager]
---

# TASK
GOAL: <High-impact capability or architectural change>
DONE WHEN: <Full verification matrix pass + staging promoted>
TARGET: <Declared module or subsystem>

# SCOPE & CANDIDATE FREEZE
Operate exclusively on:
- path: <allowed_path_1>
- path: <allowed_path_2>

Frozen candidate: <commit_hash_or_version_tag>
Allowed delta: Modifications strictly confined to declared paths.

# GATED LIFECYCLE
1. STAGING: Write all generated outputs first to `staging/<run_id>/`.
2. VERIFICATION: Execute `<full_suite_command>`.
3. PROMOTION: Promote staging to production target only after validation PASS.
4. ROLLBACK: If verification fails, discard staging and leave production target unchanged.

# HUMAN DECISION ENVELOPE
If a blocking design choice or ambiguous policy is encountered, STOP and emit:
```yaml
human_decision_required:
  reason: "<why execution is blocked>"
  question: "<concise decision question>"
  options:
    - id: A
      description: "<option description>"
      effect: "<consequence of choosing A>"
    - id: B
      description: "<option description>"
      effect: "<consequence of choosing B>"
```

# RETURN CONTRACT
Conclude with this block:
```yaml
result_receipt:
  status: done | blocked | failed | rolled_back
  summary: "<one sentence summary>"
  candidate_sha: "<sha>"
  staged_artifacts: [<paths>]
  promoted_artifacts: [<paths>]
  evidence:
    - command: "<command>"
      exit_code: 0
  human_decisions_logged: []
  residual_risks: []
```
```

---

## 4. FULL_ANTIDRIFT Profile (Benchmarks / Adversarial Audit / Long Episodes)

```markdown
---
protocol: agent-dispatch/v1
profile: FULL_ANTIDRIFT
role: evaluator_or_executor
not_role: [orchestrator, sovereign_decision_maker]
---

# TASK & BENCHMARK IDENTITY
GOAL: <Audited evaluation or benchmark comparison>
DONE WHEN: <E2E evidence matrix complete with zero evidence contamination>
EXPERIMENTAL CONDITION:
  model: <model_name>
  harness: <harness_version>
  toolset: <tools_enabled>
  dataset: <frozen_dataset_id>

# EVIDENCE INTEGRITY GATES
- Zero Contamination: Preserve candidate immutability during evaluation.
- Official Interfaces: Operate strictly via official interfaces available to target users.
- Frozen Inputs: Maintain immutable inputs and tool definitions throughout the run.

# ANTIDRIFT MONITORING
Watch for and abort on:
- Goal Drift: Work deviating from declared benchmark rubric.
- Scope Drift: Accessing files outside the frozen dataset.
- Claim Drift: Emitting positive claims without matching command exit codes.

# RETURN CONTRACT
Conclude with this block:
```yaml
result_receipt:
  status: done | degraded | failed | invalid_run
  summary: "<one sentence summary>"
  evidence_integrity: VALID | DEGRADED | INVALID
  benchmark_metrics:
    total_cases: 0
    passed: 0
    failed: 0
  evidence_matrix:
    - case_id: "<id>"
      command: "<command>"
      exit_code: 0
      integrity_status: VALID
  residual_risks: []
```
```

---

## 5. JSON A2A RPC Mode (High-Efficiency Single-Payload Envelope)

For programmatic worker dispatch via tools, APIs, or subprocess stdin:

### A. CONTROLLED Request Payload (JSON)

```json
{
  "protocol": "agent-dispatch/v1",
  "profile": "CONTROLLED",
  "role": "executor",
  "not_role": ["orchestrator", "approver"],
  "task": {
    "goal": "<observable final state>",
    "done_when": "<observable completion condition>",
    "target": "<bounded subsystem or file>"
  },
  "scope": {
    "allowed_paths": ["<path_1>", "<path_2>"],
    "ownership_policy": "fail_closed_scoped"
  },
  "frozen_context": {
    "working_directory": "<abs_path>",
    "baseline_sha": "<commit_hash>"
  },
  "gates": {
    "pre_flight": ["check_tool_exists", "verify_pwd"],
    "validation": {
      "command": "<exact test command>",
      "expected_exit_code": 0
    }
  },
  "hard_stops": [
    {
      "trigger": "missing_secret_or_env",
      "action": "stop_and_block"
    },
    {
      "trigger": "scope_breach",
      "action": "stop_and_block"
    }
  ],
  "response_format": "json_receipt"
}
```

### B. Minified Compact String (for extreme token efficiency)

```json
{"protocol":"agent-dispatch/v1","profile":"CONTROLLED","role":"executor","not_role":["orchestrator","approver"],"task":{"goal":"<goal>","done_when":"<condition>"},"scope":{"allowed_paths":["<path>"]},"gates":{"validation":{"command":"<cmd>","expected_exit_code":0}},"response_format":"json_receipt"}
```

