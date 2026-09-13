# L2 Gated Prompting Template

Verbatim 9-gate template for local agents, automated runners, and repository automation.

```markdown
# TASK
<Describe a single, bounded, and executable task. Specify the exact desired end state.>

# CONTEXT
<Provide only context necessary for THIS specific agent. Do not include instructions intended for other tools or conversational assistants.>

# SCOPE
Allowed:
- <Explicitly permitted paths, directories, commands, and systems>
Forbidden:
- <Explicitly forbidden paths, files, dangerous commands, or out-of-bounds resources>
Out of scope:
- <Adjacent work that must NOT be attempted in this turn even if convenient>

# AUTHORITY GATE
Before executing, declare:
- Execution owner: <Agent ID / script name>
- Decision owner: <Human operator / Orchestrator>
- Authoritative state source: <File path, database, or branch representing source of truth>
- Non-authoritative evidence surfaces: <Logs, stdout, test results, reports>
Fail fast if authority is ambiguous, conflicting, or duplicated.

# RUNTIME DISCOVERY GATE
Verify environment before applying any changes:
- Required CLI binaries exist on PATH with verified absolute paths
- Tool versions match compatibility requirements
- Working directories and repository root are detected and confirmed
- Read/write permissions on working directories are verified
- Required secrets and environment variables are present (without echoing values)
- Baseline state is recorded (e.g. `git status --porcelain`, baseline hash)

# SECRET HANDLING GATE
- Secrets must never be logged, echoed, committed, or persisted in artifacts.
- Fail closed immediately if an essential secret or credential is missing.

# OWNERSHIP GATE
- Exactly one process or agent owns each mutated state surface or file.
- Reject concurrent or uncoordinated mutations on shared files.

# LIFECYCLE / CRASH-SAFETY GATE
- Explicit state transitions: `initial` -> `in_progress` -> `promoted` / `failed` / `rolled_back`.
- Staging strategy: all intermediate writes MUST go to an isolated staging directory (e.g. `staging/<run_id>/`) or temporary branch/worktree.
- Promotion strategy: atomic move/swap only after all validation gates pass.
- Rollback strategy: restore baseline snapshot if any gate fails or execution aborts.

# VALIDATION GATE
Define PASS criteria in strictly objective, executable terms:
- Concrete command to run (e.g. `npm test`, `pytest tests/`, `shellcheck script.sh`)
- Expected exit code (e.g. 0)
- Expected output artifact or log assertion
- At least one boundary, regression, or negative test case verified

# DEGRADATION / REGRESSION GATE
- Measure before vs. after metrics (e.g. test count, file count, latency threshold).
- Block promotion if regression occurs (e.g. dropped tests, increased lint errors).

# OBSERVABILITY GATE
Every run must produce an auditable receipt:
- Unique `run_id` and start/finish ISO timestamps
- Process exit codes and log file pointers
- Diff summary and before/after stats
- Diagnostic artifact for troubleshooting upon failure

# CLAIM DISCIPLINE GATE
- Never claim "PASS", "stable", "complete", or "safe" without citing verifiable evidence.
- Each claim must cite: command run + exit code + generated artifact path.
- Enumerate all residual risks and unverified assumptions explicitly.

# DELIVERABLES
Return structured summary:
1. Executive summary of actions taken
2. Complete list of files created, modified, or deleted
3. Commands executed with exit codes
4. Links/paths to evidence artifacts
5. Gate status checklist (PASS / FAIL / WAIVED with reason)
6. Residual risks and pending decisions
```
