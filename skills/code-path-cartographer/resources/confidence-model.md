# Confidence Model

Rules for classifying connectivity findings. Every edge in the call graph
must have a confidence level.

## Levels

### HIGH — Full Static Trace

The reference is a direct, verifiable call in source code.

**Criteria:**
- Static function/method call: `auth_service.login()`
- Direct import used: `from auth import login`
- Explicit reference: `obj.method_name()`
- Adapter resolved the call chain end-to-end (e.g., Trifecta graph)

**Allowed language:**
- "is connected to"
- "is reachable from"
- "calls" / "called by"
- "imports" / "imported by"

**Prohibited:**
- "is the only path" (can't know without exhaustive search)
- "must be called" (could be dead branch)

### MEDIUM — Connected with Dynamic Gap

A connection exists but passes through a dynamic dispatch mechanism.

**Criteria:**
- Plugin/registry pattern: `registry[name]()`
- Reflection: `getattr(obj, method_name)`
- Strategy pattern: `strategy.execute()` where strategy is injected
- Event system: `emit("event_name")` with listener lookup
- Factory: `Factory.create(type_name)`
- String dispatch in config files

**Allowed language:**
- "likely connected to"
- "probable path via [mechanism]"
- "reachable through dynamic dispatch"

**Prohibited:**
- "is connected to" (without qualifier)
- "definitely calls"

### LOW — Inference Only

No code trace supports the connection. Based on naming, convention, or
heuristic.

**Criteria:**
- Symbol name matches a pattern but no import/call found
- Referenced only in comments or documentation
- Similar naming to a connected symbol (possible rename leftover)
- Present in a directory of related modules but not imported
- Config value matches a class name but no explicit loading code found

**Allowed language:**
- "may be connected"
- "candidate for [classification]"
- "no static trace found"

**Prohibited:**
- "is connected"
- "likely connected"
- "dead code"
- "unused"
- "safe to delete"
- "orphaned"

## Language Rules (All Levels)

### Always Prohibited

| Phrase | Why |
|--------|-----|
| "dead code" | Requires authority verdict |
| "unused" | Ambiguous — imported-but-uncalled is different from unreferenced |
| "safe to delete" | Requires authority + impact analysis |
| "orphaned" | Authority-flow-audit term |
| "should be removed" | Actionable verdict, not a fact |
| "definitely" / "certainly" | Overstates static analysis |

### Always Required

- State the confidence level explicitly
- State the evidence type: static-trace / dynamic-gap / inference / naming
- If MEDIUM or LOW, explain the gap

## Confidence Assignment Flow

```
reference_found?
  ├─ YES → is it a direct call/import?
  │         ├─ YES → HIGH
  │         └─ NO → is it dynamic dispatch?
  │                  ├─ YES → MEDIUM
  │                  └─ NO → LOW (naming/convention only)
  └─ NO → search failed or no reference?
           ├─ search failed → mention as limitation, don't classify
           └─ no reference → HIGH for "unwired" if symbol exists
```

Note: "unwired" (not referenced) gets HIGH confidence that it IS unwired,
not HIGH confidence that it IS dead. The distinction matters.
