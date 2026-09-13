# Artifact Retrieval Reference

Full pseudocode for artifact retrieval by store mode. Loaded during Phase 1 of the gate.

## Mode Detection

```
# Check for config in order: openspec/config.yaml > env var > default
if exists("openspec/config.yaml"):
    mode = read("openspec/config.yaml").get("artifact_store", "hybrid")
else if env("SDD_ARTIFACT_STORE"):
    mode = env("SDD_ARTIFACT_STORE")
else:
    mode = "hybrid"  # default
```

## Retrieval by Mode

```
# ENGRAM-ONLY MODE
if mode == "engram":
    spec_content   = mem_search("sdd/{change-name}/spec")    → mem_get_observation(id)
    design_content = mem_search("sdd/{change-name}/design")   → mem_get_observation(id)
    tasks_content  = mem_search("sdd/{change-name}/tasks")    → mem_get_observation(id)
    # NO filesystem fallback — error if not found

# OPENSPEC-ONLY MODE  
elif mode == "openspec":
    spec_content   = read("openspec/changes/{change-name}/specs/.../spec.md")
    design_content = read("openspec/changes/{change-name}/design.md")
    tasks_content  = read("openspec/changes/{change-name}/tasks.md")
    # NO engram fallback — error if not found

# HYBRID MODE (default)
else:  # mode == "hybrid"
    # Try engram first, fall back to filesystem
    spec_content   = mem_search("sdd/{change-name}/spec")    → mem_get_observation(id)
    if not spec_content:
        spec_content = read("openspec/changes/{change-name}/specs/.../spec.md")
    # ... same for design_content, tasks_content
```

## Graceful Degradation

Proceed with available artifacts only. Inform agents which artifacts are absent. Error only if spec is missing entirely.

## Input Size Limits

If any artifact exceeds 50,000 characters or 2,000 lines, warn and suggest simplification before dispatching agents.
