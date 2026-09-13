# Prompt Template

Write to `/tmp/fork-prompt-<name>.txt`:

```markdown
## Role
<explorer|implementer|verifier|architect|analyst>

## Task
<Specific, bounded task. Include file paths.>

## Context
<Key files, patterns, constraints.>

## Deliverable
<What the agent must produce. File path or stdout format.>

## Constraints
- Time limit: <seconds>
- Output to: <file path or format>
- Do NOT modify: <protected files>
```

## Tips

- Keep tasks bounded and specific — fork agents work best with clear scope
- Include file paths in Context so agents don't waste time searching
- Set explicit output paths in Deliverable for easy consolidation
- Use `constraints` to protect files that shouldn't be modified
- Role determines model assignment (see SKILL.md Role → Model table)
