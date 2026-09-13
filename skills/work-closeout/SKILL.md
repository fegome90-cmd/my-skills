---
name: "work-closeout"
description: "Trigger: close out, clean temporary files, /work-closeout. Explore, report, and quarantine proven residue with a durable receipt."
license: MIT
metadata:
  author: "Felipe Gonzalez"
  version: "1.1.0"
disable-model-invocation: true
argument-hint: "[inspect|dry-run|apply|restore|recover] [scope]"
---

# Work Closeout

Close a completed work unit with low-friction exploration, evidence-backed classification, reversible quarantine, and a verification receipt. Let the agent investigate and explain candidates without mutation; reserve governance friction for the exact batch that will change the filesystem.

## Workflow

1. **Resolve the operation.** Interpret the invocation as `inspect`, `dry-run`, `apply`, `restore`, or `recover`; default to `inspect`. Read the canonical R7 contract and `references/clean-workbench-reset.v1.json` before classifying. Complete this step when the operation, scope, profile, and v1 boundary are explicit.

2. **Explore without approval.** For `inspect`, scan the explicit scope without following links, capture the baseline, and produce a decision report. For `dry-run`, freeze the sorted candidate report and predicted manifest. Do not request approval and do not mutate files in either mode. Complete this step when every scanned entry is classified as eligible, keep, protected, or ambiguous, with evidence and reason codes.

3. **Separate proposal from eligibility.** Let the LLM summarize evidence and explain likely residue, but never treat confidence, filename, extension, age, size, or appearance as authorization. Only `TEMPORARY` and `GENERATED_ARTIFACT` candidates with all required evidence may enter the action manifest; report suspected and ambiguous items as `KEEP` or `AMBIGUOUS_REVIEW`. Complete this step when the report distinguishes proposed quarantine from no-touch outcomes.

4. **Ask once for the exact batch.** Present grouped candidates, risks, exclusions, predicted receipt, and manifest digest. Require approval only when `apply` has a non-empty manifest; bind it to the resource, profile, scope, baseline, policy, manifest, candidate IDs, principal, nonce, and expiry. Complete this step when the approval matches the frozen manifest or the run becomes inspect-only.

5. **Acquire execution guards.** Acquire the R7 exclusive scope lock, verify fencing, probe no-replace support, and revalidate digests, containment, protected roots, link/special-file status, source preconditions, and destination absence immediately before mutation. Record memory only as evidence with `authorizes: false`. Complete this step when every guard passes or the receipt records an inspect-only block.

6. **Apply transactionally.** Journal each action, perform only same-filesystem no-replace moves into quarantine, preserve bytes/metadata/identity, and write durable completion boundaries. Use the R7 recovery table for restore/recover; do not improvise recovery from labels. Complete this step when each action result and journal prefix match physical state.

7. **Verify and finalize.** Re-scan source and destination, recompute bytes, size, hashes, metadata, identities, and protected-root invariants, then finalize the R7 receipt plus the clean-workbench receipt link. Release the lock only after finalization. Complete this step when receipt, journal, memory evidence, lock status, and observed run state agree.

8. **Dogfood before claiming readiness.** On a disposable fixture with explicit provenance, run `apply` and `restore`; verify source/destination transitions, no-replace behavior, byte/hash/metadata/identity parity, and cleanup. Discover host-specific filesystem capabilities before execution and fail closed when a capability or receipt invariant is unavailable. Complete this step when the end-to-end receipt is independently verified; otherwise report the skill as inspect/dry-run ready only.

9. **Preserve the boundary.** Keep documents and filenames unchanged. Keep permanent deletion, global disk cleanup, vault/Git/PR mutation, network effects, cross-filesystem copy, classifier learning during apply, and memory authorization outside this skill. Complete this step when the report states scope, candidates, actions, verification, memory outcome, restore path, and blockers.

## Resources

- `references/clean-workbench-reset.v1.json` — decision/report resource for the three-layer explore → report → approve/apply workflow; read before candidate classification.
- `templates/closeout-receipt.yaml` — mandatory R7 receipt shape.
