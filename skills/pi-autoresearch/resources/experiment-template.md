# Experiment Template

Hypothesis-prediction-result format for autoresearch-gate experiments.

## Format

Every experiment in autoresearch-gate follows this structure:

```
OPPORTUNITY: O-<N>: <title>
HYPOTHESIS: If <action>, then <expected outcome>
PREDICTION: <metric_name> will change from <baseline_value> to <predicted_range>
EXPERIMENT: <command that proves or disproves the hypothesis>
RESULT: <metric_name> = <actual_value> — PASS/FAIL
```

## Example: O-1 Class→Method Path Gap

```
OPPORTUNITY: O-1: Class→method path expansion
HYPOTHESIS: If BFS auto-expands class nodes to their methods when traverse_classes=True,
  then class-level paths that currently fail will succeed
PREDICTION: features_validated will change from 3 to 5 (+66.7%)
EXPERIMENT: cd paper-writer && uv run python -c "
  gs = GraphService()
  pairs = [('main','GateResult'), ('Orchestrator','GateResult'),
           ('main','Orchestrator'), ('Orchestrator.execute','GateResult'),
           ('BibliographyNormalizer','ToolWrapper')]
  passes = sum(1 for s,d in pairs if gs.path(root,s,d)['path_exists'])
  print(f'features_validated={passes}/5')
"
RESULT: features_validated = 5 — PASS
```

## Example: O-5 Impact Analysis

```
OPPORTUNITY: O-5: Reverse path / impact analysis
HYPOTHESIS: If we add reverse BFS (find_upstream) across all edge kinds with
  ImpactPredicate NL patterns, users can query blast radius from natural language
PREDICTION: nl_patterns_matched will change from 2 to 9, reverse_path_api from 0 to 1
EXPERIMENT: cd paper-writer && uv run python -c "
  oracle = SearchOracleUseCase(...)
  queries = ['impact of changing GateResult', 'what relies on ToolWrapper', ...]
  matched = sum(1 for q in queries if oracle.execute(root,q).fidelity == 'full')
  print(f'nl_patterns_matched={matched}')
"
RESULT: nl_patterns_matched = 9, reverse_path_api = 1 — PASS
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| Vague hypothesis ("it will work") | No way to falsify — always "works" | Be specific: metric name, expected range |
| Prediction = same as hypothesis | Circular reasoning | Prediction is NUMERIC: baseline → target range |
| Experiment tests something else | Validation gap | Use the SAME validation as baseline |
| No PASS/FAIL threshold | Everything "looks good" | Define threshold before running |
| Skip baseline in hypothesis | Cannot measure delta | Always include baseline value |
| Multiple hypotheses per experiment | Confounds result | One hypothesis per experiment cycle |

## Hypothesis Quality Checklist

Before running the experiment, verify:

- [ ] Hypothesis has a clear IF-THEN structure
- [ ] Prediction includes exact metric name and numeric range
- [ ] Baseline value is from a prior logged experiment
- [ ] Experiment command is copy-paste-runnable
- [ ] PASS/FAIL threshold is explicit (not "eyeball it")
- [ ] Only ONE hypothesis is being tested