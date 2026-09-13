# Known False-Positive Patterns

These patterns commonly trigger false positives during SDD gate analysis. Agents MUST cross-reference findings against this table before reporting.

## Pattern Reference Table

| # | Pattern | Why It Triggers | Typical Finding | Why It's Usually Valid | Verification Action |
|---|---------|----------------|----------------|----------------------|---------------------|
| 1 | **dataclass.asdict** | `asdict()` serializes all fields including internal state | "Sensitive data exposed in serialization" | Frozen dataclasses with controlled fields are intentional — `asdict` is the standard serialization path | Check if dataclass has `frozen=True` and fields are typed. If yes, DISCARD. |
| 2 | **Migration idempotency** | Migration functions appear to "run every time" | "Migration will re-execute on every startup" | Migration runners track executed migrations via version tables — idempotency is the design intent | Check if migration framework uses version tracking (Alembic, Prisma, Django). If yes, DISCARD. |
| 3 | **Keyword-args constructors** | All constructor arguments passed as keyword arguments | "Redundant parameter passing" | Keyword-only constructors enforce API clarity and are a Python best practice (PEP 3102) | Check if constructor uses `*` separator or TypedDict/Pydantic model. If yes, DISCARD. |
| 4 | **Container init timing** | Dependencies initialized lazily inside functions | "Race condition in dependency initialization" | Lazy initialization in DI containers is intentional — avoids circular imports and startup overhead | Check if container uses `@lru_cache`, singleton pattern, or lazy proxy. If yes, DISCARD. |
| 5 | **Exception handling** | Generic `except Exception` with re-raise | "Overly broad exception handling" | Pattern `except Exception as e: log(e); raise` is standard for observability — not swallowing | Check if exception is re-raised after logging. If yes, DISCARD. Only report if exception is swallowed silently. |

## Usage by Agents

When an agent identifies a potential finding that matches a pattern above:

1. **Check the Verification Action** column for the specific verification step
2. **Apply the verification** against the actual artifact content
3. **If verification confirms intentional use** → increment `findings_discarded`, do NOT report
4. **If verification reveals genuine issue** → report with evidence quote showing the problem

## Adding New Patterns

When a new false-positive pattern is identified across multiple runs:

1. Add entry to this table with: pattern name, trigger reason, typical finding, why it's valid, verification action
2. Keep patterns codebase-agnostic (domain patterns, not project-specific)
3. Maximum recommended: 10 patterns (beyond that, review for removal of obsolete entries)
