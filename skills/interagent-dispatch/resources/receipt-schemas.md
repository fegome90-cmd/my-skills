# Receipt Schemas and Validation

This reference defines the schemas and parsing rules for worker return receipts.

---

## 1. Minimal Receipt Schema (YAML)

```yaml
result_receipt:
  status: done | partial | blocked | failed
  summary: "<concise 1-sentence outcome>"
  modified_files:
    - "<path_to_file>"
  evidence:
    - command: "<command_executed>"
      exit_code: 0
  blocking_reasons: []
  residual_risks: []
```

---

## 2. Full Evaluation Receipt Schema (JSON)

```json
{
  "result_receipt": {
    "status": "done",
    "summary": "Implemented auth middleware with test coverage",
    "candidate_sha": "7f8b9c2",
    "modified_files": [
      "src/auth/middleware.ts",
      "tests/auth/middleware.test.ts"
    ],
    "evidence": [
      {
        "claim": "All 8 unit tests pass",
        "command": "bun test tests/auth/middleware.test.ts",
        "exit_code": 0,
        "evidence_integrity": "VALID"
      }
    ],
    "blocking_reasons": [],
    "residual_risks": [
      "Token expiry under clock skew is untested"
    ]
  }
}
```

---

## 3. Compact JSON Response Receipt (Machine Parseable)

```json
{
  "result_receipt": {
    "status": "done",
    "summary": "<1-sentence summary>",
    "modified_files": ["<path>"],
    "evidence": [
      {
        "command": "<cmd>",
        "exit_code": 0
      }
    ],
    "blocking_reasons": [],
    "residual_risks": []
  }
}
```

---

## 4. Human Decision Envelope Schema (YAML / JSON)

When execution is blocked pending an architectural, destructive, or policy decision:

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

---

## 5. Orchestrator Validation Rules

When the worker returns:

1. **Schema Validation & Required Fields:** Ensure the payload contains the `result_receipt` root object and parses cleanly. Enforce presence of all required fields: `status` (enum: `done`, `partial`, `blocked`, `failed`), `summary` (string), `modified_files` (list of strings), `evidence` (list of objects), `blocking_reasons` (list), and `residual_risks` (list). Missing fields or schema non-conformance fail closed to `status: failed`.
2. **Evidence Iteration & Status Integrity:** Iterate across all entries in `evidence`. If any item has `exit_code != 0` or missing command output, reject `status: done` (fail-closed to `status: failed`).
3. **Scope Integrity:** Compare `modified_files` against `scope.allowed_paths`. Any out-of-scope mutation triggers immediate block.
4. **Claim Alignment:** Verify that every claim in `summary` maps to at least one verified item in `evidence` with `exit_code: 0`.
5. **Decision Escalation:** When `human_decision_required` is returned, halt autonomous execution and present the decision envelope to the user.

