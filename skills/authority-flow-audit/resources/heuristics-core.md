# Core Detection Heuristics (H1-H5)

The 5 highest-frequency patterns. Always load during Phase 5.

---

### H1: Multiple Entrypoints → Same Mutation

**Pattern:** Two or more surfaces can trigger the same state mutation through different
code paths.

**Detect:** Identify a mutation → trace all callers to entrypoints → flag if >1 entrypoint.

**Confirm:** Grep for write function name, trace each call site to root, check validation
differences between entrypoints.

**Severity:** HIGH (uncoordinated) / MEDIUM (shared validation)

**Example:**
```
API PUT /users/:id → update_user()
CLI user update → update_user()
Cron sync_users → update_user()
```
Three entrypoints, one mutation. If any skips validation, others' guarantees break.

---

### H2: Script/CLI Bypass of Official Path

**Pattern:** A script or CLI duplicates an official pipeline but without its validation,
auth, or lifecycle hooks.

**Detect:** Catalog scripts in `scripts/`, `bin/`, `tools/` → identify state I/O →
cross-reference with official API/service methods → flag if script does raw I/O.

**Confirm:** Read script source → check if it imports official service or does raw I/O
→ check if it has its own validation (likely different).

**Severity:** HIGH

**Example:**
```
scripts/force-sync.sh writes directly to DB
API POST /sync calls sync_service.sync() with validation
→ bypass
```

---

### H3: Hook/Job Mutates State Outside Lifecycle

**Pattern:** A lifecycle hook or scheduled job mutates state the main application also
manages, creating double-execution or race conditions.

**Detect:** List hooks and jobs → map state mutations → cross-reference with normal
app flow → flag overlap → check coordination.

**Confirm:** Check if hook/job runs while app is active → check locking/idempotency →
check if mutations are visible to app.

**Severity:** CRITICAL (concurrent) / HIGH (sequential uncoordinated)

---

### H4: Double Writer on Same File/Table

**Pattern:** Two surfaces write to the same file or DB table without coordination,
risking corruption or race conditions.

**Detect:** For each state artifact, list all writers → if >1, check coordination
(file locking, DB transactions, mutex, sequential scheduling) → flag if none.

**Confirm:** Grep all write ops to target → check locking primitives → check if
concurrent execution is possible.

**Severity:** CRITICAL

---

### H5: Evidence Used as Authority

**Pattern:** A log, report, metric, or test result is used as the basis for a state
decision when it should only be observational. This is the most common SSOT violation:
an evidence surface becomes a de facto authority because downstream surfaces depend on it.

**Detect:** Identify evidence surfaces (logging, reporting, monitoring) → trace if other
surfaces read evidence to make state decisions → flag if production surface reads
log/report to decide writes.

**Confirm:** Check if downstream surfaces depend on log/report output format → check
if location is configurable (fragile dependency) → check if producer knows it is consumed.

**Severity:** HIGH

**Example:**
```
Job A writes status log to /tmp/pipeline-status.log
Job B reads /tmp/pipeline-status.log to decide whether to run
→ Job B treats evidence as authority. If log format changes, Job B breaks.
```
