# Opportunity Validation Procedure

Detailed procedure for the autoresearch-gate skill's implement and validate modes.

## Implement Mode (Full Flow)

### Phase 1: Baseline

**Goal**: Quantify the current state before any change. No baseline = no implementation.

1. Initialize autoresearch session:
   ```
   init_experiment(
     name="O-<N>: <opportunity title>",
     metric_name="<primary metric>",
     metric_unit="<unit or ''>",
     direction="higher|lower"
   )
   ```

2. Write a validation script that exercises the gap. The script MUST:
   - Import only application-layer code (GraphService, OracleUseCase)
   - Print structured output: `key=value` pairs for each check
   - Exit 0 on success, non-zero on failure
   - Be runnable from the target repo directory

3. Run baseline:
   ```
   run_experiment(command="cd <repo> && uv run --active python -c '<validation_script>'")
   ```

4. Log baseline:
   ```
   log_experiment(
     commit="<git hash>",
     description="Baseline: <what the gap is, quantified>",
     metric=<value>,
     status="keep"
   )
   ```

5. If baseline shows no gap (e.g., all paths already work), **STOP**. The opportunity may be stale.

6. Save baseline observation to engram:
   ```
   memory_save(
     content="<O-N baseline: N failures, M successes, root cause>",
     type="discovery",
     what="O-N baseline measurement",
     why="Quantifies the problem for validation"
   )
   ```

### Phase 2: Ask-on-Risk

**Goal**: Choose the implementation approach with lowest risk. See `resources/risk-matrix.md` for scoring framework.

1. List 2-4 implementation options. For each, identify:
   - Invasiveness: Does it change stored data? Graph structure? Public API?
   - Re-indexing: Does it require re-running the indexer?
   - Backward compatibility: Will existing callers break?
   - Test surface: How many new tests needed?

2. Score each option using risk-matrix framework.

3. Pick the lowest-risk option that solves the problem.

4. If the "obvious" option scores high-risk, explicitly document WHY a less obvious option was chosen.

5. Record to engram:
   ```
   memory_save(
     content="O-N decision: Option X chosen because <rationale>",
     type="decision",
     what="Implementation approach for O-N"
   )
   ```

### Phase 3: Implement + Validate

**Goal**: Write code and prove it works with the same experiment.

1. Implement the chosen option. Commit mentally to rolling back if validation fails.

2. Run the SAME validation script from Phase 1:
   ```
   run_experiment(command="cd <repo> && uv run --active python -c '<same_script>'")
   ```

3. **Validation gates** (all must pass to proceed):
   - Primary metric improved vs baseline
   - Zero test regressions (run full unit suite)
   - Zero new code errors (LSP diagnostics or type check)
   - Validation script exit code = 0

4. If ANY gate fails:
   - Rollback: `git stash` or manual revert
   - Try next option from Phase 2, or
   - STOP and report the blocker

5. Add new unit tests for the implemented feature. Target: ≥2 tests per new capability.

6. Run full regression suite:
   ```
   run_experiment(command="cd <project> && uv run pytest tests/unit/ -q --tb=short")
   ```

### Phase 4: Persist

**Goal**: Lock in the validated result.

1. Log experiment result:
   ```
   log_experiment(
     commit="<git hash>",
     description="O-N RESOLVED: <what was done, key numbers>",
     metric=<new_value>,
     status="keep"
   )
   ```

2. Git commit with structured message:
   ```
   O-N: <title>
   - <key change 1>
   - <key change 2>
   - <metric delta>
   - N new tests, M total pass, 0 regressions
   ```

3. Save lesson to engram:
   ```
   memory_save(
     content="O-N resolved: <approach>. Key lesson: <takeaway>",
     type="decision"
   )
   ```

4. Update roadmap: mark opportunity as Done with result summary.

5. Clean up temporary files or debug code.

### Phase 5: Next

Return to Phase 1 for the next highest-priority opportunity. The autoresearch loop continues until interrupted or backlog is empty.

## Validate Mode (Read-Only)

**Goal**: Measure the current state without changing code. Used for: gap analysis, backlog prioritization, pre-implementation research.

1. Run Phase 1 (Baseline) as above.
2. Run Phase 2 (Ask-on-Risk) as above — document the recommended approach without implementing.
3. Produce a **validation report**:
   ```
   VALIDATION REPORT: O-N
   =====================
   Metric: <name> = <value> (direction: higher/lower)
   Gap: <description of what's missing>
   Recommended approach: Option X (risk score: N)
   Alternatives considered: A (score N), B (score N)
   Estimated effort: <hours>
   Priority: <high/medium/low>
   ```

4. No git commit, no code changes. Save to engram as discovery.

## Rollback Protocol

When Phase 3 validation fails:

| Severity | Action |
|----------|--------|
| Test regression | `git checkout -- <files>` for changed files. Retry with different approach. |
| Metric did not improve | Keep code if no regressions. Try complementary approach for next iteration. |
| New code errors introduced | Full `git stash`. Do not proceed until errors are understood. |
| Crash / hang | Kill process. `git stash`. Investigate root cause before retry. |

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Skip baseline | No way to prove improvement | Always run baseline first |
| Skip risk assessment | Choose "obvious" option that creates debt | Score all options |
| Change validation script | Apples-to-oranges comparison | Use identical script |
| Add features during implement | Scope creep, unvalidated changes | One opportunity per loop |
| Commit without log_experiment | Lost provenance | Log before commit |