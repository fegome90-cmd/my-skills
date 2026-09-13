# Anti-Patterns in Agent Prompting

The four canonical failure modes when prompting autonomous or local agents, along with concrete corrections.

---

## 1. Gate Without Mechanism

### The Mistake
Using subjective, declarative instructions like:
- *"Asegurate de que todo funcione correctamente y sea seguro."*
- *"Valida los cambios y confirmá que el código esté listo para producción."*

### Why It Fails
Agents interpret subjective statements as permission to declare success based on internal confidence rather than external evidence. Without a deterministic mechanism, agents hallucinate verification.

### The Correction
Map every gate to a concrete command, exit code, and artifact assertion:
```markdown
# VALIDATION GATE
Command: `pytest tests/test_core.py -v`
Expected: exit code 0, 0 failures, total tests >= 15.
Assertion: Output contains "15 passed in".
```

---

## 2. Audience Mixing

### The Mistake
Mixing conversational framing, meta-reasoning, human instructions, and agent shell tasks in the same prompt block:
- *"Como experto en arquitectura, explicame el problema, luego abrí una terminal, corré git status y actualizá el archivo."*

### Why It Fails
The local agent becomes confused about its role—often writing an essay explaining the command to the user rather than running the command, or executing actions meant only as illustrative examples.

### The Correction
Strictly isolate audiences:
- **Consulting / Prompting Analyst:** Methodology, trade-offs, architecture review criteria, reasoning.
- **Local Agent / Executor:** Executable task description, strict path whitelists, CLI commands, expected artifacts.
- **System / Repo:** Hard state contracts, schema validation, git commits.

---

## 3. Strong Claims Without Evidence

### The Mistake
Allowing agents to claim perfection without proof:
- *"El sistema quedó 100% probado, estable y listo para producción."*
- *"Todos los casos bordes fueron resueltos."*

### Why It Fails
Creates dangerous false confidence. When unexpected edge cases or crashes occur in production, there is no audit trail of what was actually tested and what was merely assumed.

### The Correction
Enforce strict claim discipline:
```markdown
# CLAIM DISCIPLINE GATE
Report strictly:
- Observed PASS: `pytest -q` (exit code 0), `dist/bundle.js` created (45.2 kB).
- Not proven: Concurrency under >100 req/s, recovery from SIGKILL.
- Residual risk: Upstream third-party API rate limits remain unmocked in test suite.
```

---

## 4. Implicit Staging & Direct Mutation

### The Mistake
Instructing agents to directly overwrite live configuration files, source trees, or databases during exploratory or non-validated tasks:
- *"Modificá config.json directamente y regenerá la base de datos."*

### Why It Fails
If any intermediate step fails, crashes, or produces invalid syntax, the system is left in a broken, half-migrated state with no clean recovery path.

### The Correction
Enforce explicit staging and transactional promotion:
```markdown
# LIFECYCLE GATE
1. Write all modified files to `staging/<run_id>/`.
2. Validate staging outputs with `validate-schema --file staging/<run_id>/config.json`.
3. Promote atomically (e.g. `mv` or atomic rename) ONLY after validation exit code is 0.
4. On failure: abort, remove `staging/<run_id>/`, and report errors.
```
