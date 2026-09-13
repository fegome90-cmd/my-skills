# Extended Detection Heuristics (H6-H13)

Load when deeper analysis is needed beyond the core 5 patterns.

---

### H6: Wrapper That Shadows Authority

This consolidates two related patterns: wrappers that reimplement logic instead of
delegating, and surfaces that appear delegated but perform hidden side effects.

**Pattern:** A wrapper function, decorator, or middleware claims to delegate to an inner
surface but either reimplements core logic or adds undocumented side effects, creating
shadow authority or hidden mutations.

**Detect:** Find wrappers (functions that call another with same/similar purpose) →
compare wrapper body with wrapped function → flag if wrapper adds business logic,
extra mutations, or undocumented I/O beyond cross-cutting concerns.

**Confirm:**
- For reimplementations: diff wrapper vs wrapped → check mutation differences → check
  if wrapper is called in some paths but wrapped function in others
- For hidden side effects: read full body → compare with delegate's contract → check
  if side effects are documented or intentional

**Severity:** HIGH (extra mutations) / MEDIUM (read-only side effects like logging)

**Example:**
```python
def save_report(report):
    validate(report)
    db.save(report)

def save_report_wrapper(report):
    log.info("Saving report")
    custom_validate(report)  # different validation — reimplements logic
    db.save(report)          # bypasses official save_report()
    notify_slack(report)     # hidden side effect not in delegate contract
```

---

### H7: Fallback That Breaks SSOT

**Pattern:** A fallback path writes state that the primary path also writes, creating
two potential sources of truth depending on which path executed.

**Detect:** Find try/catch or if/else with fallback write paths → check if fallback
writes to same state as primary → check if downstream can distinguish source.

**Confirm:** Trace happy and fallback paths → check provenance metadata → check if
consumers behave differently based on source.

**Severity:** HIGH (no provenance) / MEDIUM (distinguishable)

---

### H8: Mixed Runtime Roots and State Roots

**Pattern:** Different base directories for runtime vs state persistence, surfaces
confuse one for the other.

**Detect:** Identify all base paths → classify as runtime/state/config root → check
if any surface reads from one root but writes to another of same category.

**Confirm:** Grep path constants and env vars → check if surfaces resolve same logical
path differently → check hardcoded paths.

**Severity:** MEDIUM (confusion) / HIGH (wrong-state writes)

---

### H9: Competing Script vs API vs Job for Same Artifact

**Pattern:** A script, API endpoint, and scheduled job all produce/modify the same
artifact with no declared authority. Variant of H1 focused on entrypoint type diversity.

**Detect:** For each artifact, trace producers → classify by entrypoint type → if
multiple types produce same artifact, check declared authority.

**Confirm:** Check docs vs code → check if scripts are in CI/CD (active) or just exist
→ check job schedules vs API usage.

**Severity:** HIGH

---

### H10: Legacy Pipeline Still Alive Alongside New One

**Pattern:** New pipeline replaced old one, but old still has active triggers and
produces/mutates state.

**Detect:** Search for "old", "legacy", "deprecated", "v1", "new" in comments/docs →
check if deprecated surfaces have active callers → check old job schedules.

**Confirm:** Grep deprecation markers → check cron/scheduler → check API routing →
check if old and new write to same state.

**Severity:** HIGH (both write same state) / MEDIUM (old is read-only)

---

### H11: Authority Vacuum (No Identifiable Owner)

**Pattern:** Multiple writers for an artifact, none clearly designated as authority.
This is the structural condition behind SSOT violations — detected when neither H4
(double writer) nor H5 (evidence-as-authority) fully explains the conflict.

**Detect:** For each artifact with multiple writers, check: documentation of ownership,
explicit delegation statements, naming conventions. If none hold, flag authority vacuum.

**Confirm:** Check docs/README/comments → check if any surface validates before writing
→ check if any is sole creator (vs updater) → check if ownership was never assigned
vs was assigned but drifted.

**Severity:** HIGH

---

### H12: State Read from One Source, Written to Another

**Pattern:** Surface reads from location A but writes to location B for same logical
entity, creating split-brain.

**Detect:** For each surface, note read source and write target → if different for
same logical entity, check sync mechanism.

**Confirm:** Trace full data flow → check for sync scripts/replication → check stale
read possibility.

**Severity:** CRITICAL (no sync) / MEDIUM (synced with lag)

---

### H13: Dangling Mutation / Accidental Bottleneck

Two patterns that indicate maintenance debt rather than active risk.

**Dangling mutation:** Side effect-producing function with no active callers, possibly
invoked outside version control. Severity: LOW (dead code) / HIGH (invoked outside VCS).

**Accidental bottleneck:** Serialization point treated as necessary but actually
incidental coupling that could be parallelized. Severity: MEDIUM (performance) /
LOW (architectural smell).

**Detect:**
- Dangling: for each function with side effects, trace callers → if none active, grep
  for references in scripts/cron/docs outside repo
- Bottleneck: find functions all surfaces pass through → determine if serialization is
  necessary (shared mutable state, rate limit) or accidental

**Confirm:**
- Dangling: check git history → check CI configs → check if manually invoked
- Bottleneck: check if resource could be partitioned → check if intentional → check
  if removing breaks correctness
