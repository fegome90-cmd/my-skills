---
name: "work-closeout"
description: "Trigger: close out, clean temporary files, /work-closeout. Explore, report, and classify workbench residue without destructive file mutations."
license: MIT
metadata:
  author: "Felipe Gonzalez"
  version: "1.1.0"
disable-model-invocation: true
argument-hint: "[inspect|dry-run] [scope]"
---

# Work Closeout

Close a completed work unit with low-friction exploration, evidence-backed classification, and structured reporting. The skill is strictly diagnostic and read-only: it investigates, categorizes, and explains candidate residue without mutating files, providing clear manual cleanup instructions and a verifiable audit report for the human operator.

## Workflow

1. **Resolve the operation.** Interpret the invocation as `inspect` or `dry-run`; default to `inspect`. Read `references/clean-workbench-reset.v1.json` before classifying. Complete this step when the operation, scope profile, and target path boundary are explicit.

2. **Explore without mutation.**
   - For `inspect`, scan the specified scope without traversing outside boundaries or dereferencing external symlinks.
   - For `dry-run`, sort candidate paths and predict classification groupings.
   - Do NOT execute filesystem mutations, file moves, or deletions in either mode.
   - Complete this step when every scanned entry is classified as eligible, keep, protected, or ambiguous, with recorded evidence and reason codes.

3. **Classify residue by evidence.** Evaluate candidates against `references/clean-workbench-reset.v1.json`:
   - Categorize items into `TEMPORARY`, `GENERATED_ARTIFACT`, `KEEP`, or `AMBIGUOUS_REVIEW`.
   - Never treat confidence, filename pattern, extension, age, or appearance as sole authority.
   - Report suspected, ambiguous, or unconfirmed items as `KEEP` or `AMBIGUOUS_REVIEW`.

4. **Produce audit report and receipt.**
   - Compile the candidate breakdown into a structured report using `templates/closeout-receipt.yaml` with outcome `PLANNED` or `NOOP_ALREADY_CLOSED` and verification status `NOT_RUN` for mutations.
   - Highlight eligible items with their paths, file sizes, and classification rationales.

5. **Human execution handoff.**
   - Present grouped candidates to the human operator.
   - Provide explicit, copy-pasteable manual commands (e.g. `rm`, `git clean -ndX`) for the operator to review and run if they choose.
   - Remind the operator to verify version control status (`git status`) before deleting untracked files.

6. **Preserve the boundary.**
   - Keep permanent file deletion, global disk operations, git/PR mutations, network calls, and autonomous state quarantine strictly outside this skill.
   - Complete this step when the summary clearly states inspected scope, candidate counts, classification breakdown, and recommended human actions.

## Resources

- `references/clean-workbench-reset.v1.json` — decision and classification rules for workbench residue.
- `templates/closeout-receipt.yaml` — structured report template for inspection and dry-run summaries.

