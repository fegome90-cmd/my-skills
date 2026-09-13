# Test Catalog — Memory CLI v1

This catalog lists real-world test scenarios for each CLI subsystem. Agents select scenarios matching their role and execute them against a live `memory` CLI binary.

## How to Use This Catalog

1. Pick the subsystem you are responsible for (your role).
2. Select scenarios from the table — prioritize HIGH severity first.
3. Execute the command pattern, observe behavior, classify the result.
4. Log findings to the shared results artifact.

---

## CRUD Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| C01 | Save with all flags (`--type`, `--project`, `--what`, `--where`, `--why`, `--learned`) | adversarial | HIGH | `memory save "full metadata" --type bugfix --project myproj --what fixed X --where src/x.py --why regression --learned check bounds` |
| C02 | Get by full UUID | basic | HIGH | `memory get <id>` |
| C03 | Get by 8-char prefix | basic | HIGH | `memory get <id:0:8>` |
| C04 | Update content and type | basic | MEDIUM | `memory save "updated" --type decision --topic-key <topic-key>` |
| C05 | Update project field | basic | MEDIUM | `memory save "same" -p newproj --topic-key <topic-key>` |
| C06 | Delete with `--force` | basic | HIGH | `memory delete <id> --force` |
| C07 | Upsert by topic_key | basic | MEDIUM | `memory save "upserted" --type config --topic-key my-config` then repeat with different content (should update, not duplicate) |
| C08 | Special chars in content (`' " \n ; -- `) | adversarial | HIGH | `memory save "drop table; -- 'quoted'"` |
| C09 | Unicode content (CJK, emoji, RTL) | adversarial | MEDIUM | `memory save "テスト 🧪 مرحبا"` |
| C10 | Very long content (>4KB) | chaos | MEDIUM | `memory save "$(python3 -c 'print("x"*8192)')"` |
| C11 | Metadata JSON edge cases (null fields, empty strings) | adversarial | MEDIUM | `memory save "edge" --what "" --where "" --why "" --learned ""` |
| C12 | Empty content string | adversarial | HIGH | `memory save ""` |
| C13 | Missing required args (no content at all) | basic | LOW | `memory save` |

## Search & List Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| S01 | Basic full-text search | basic | HIGH | `memory search "memory CLI"` |
| S02 | Special chars in query (`AND`, `OR`, `*`, `"`, `(`) | adversarial | HIGH | `memory search 'AND OR * "test" (nested)'` |
| S03 | Project filter on missing project | basic | MEDIUM | `memory search "x" --project nonexistent` |
| S04 | Pagination (`--limit`, `--offset`) | basic | MEDIUM | `memory search "x" --limit 1 --offset 0` |
| S05 | Empty results set | basic | LOW | `memory search "zzzzznonexistent12345"` |
| S06 | Very long query (>1KB) | chaos | MEDIUM | `memory search "$(python3 -c 'print("a "*2048)')"` |
| S07 | SQL injection attempts (`'; DROP TABLE--`) | adversarial | CRITICAL | `memory search "'; DROP TABLE memories;--"` |
| S08 | FTS5 syntax edge cases (`NEAR`, `^`, `*`) | adversarial | HIGH | `memory search 'NEAR(term1 term2, 10)'` |

## Session Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| SS01 | Start session with project | basic | HIGH | `memory session start --project myproj` |
| SS02 | Start session without project | basic | MEDIUM | `memory session start` |
| SS03 | Auto-end previous session on new start | basic | MEDIUM | Start twice, verify first ended |
| SS04 | End session without active session (wrong session) | adversarial | MEDIUM | `memory session end` when none active |
| SS05 | List sessions with project filter | basic | MEDIUM | `memory session list --project myproj` |
| SS06 | List sessions without filter | basic | LOW | `memory session list` |
| SS07 | Context recovery directive injection | adversarial | HIGH | Verify session summary contains recovery context |
| SS08 | Concurrent sessions (two terminals) | chaos | HIGH | Start session in term1, start different in term2, verify isolation |

## Sync Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| SY01 | Full export | basic | HIGH | `memory sync export` |
| SY02 | Incremental export (after changes) | basic | MEDIUM | Change data, export again, verify delta |
| SY03 | Push with simulated git failure (watermark rollback) | chaos | HIGH | Block git, push, verify watermark unchanged |
| SY04 | Pull roundtrip (export → clear → import) | basic | HIGH | Export, clear DB, import, verify data matches |
| SY05 | Status check | basic | LOW | `memory sync status` |
| SY06 | Mutation journal integrity | adversarial | MEDIUM | Mutate, check journal reflects only intended ops |
| SY07 | Project-filtered export leaks | adversarial | CRITICAL | Export with `--project A`, verify no project B data in output |

## Compact & Recovery Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| CR01 | Save summary with all fields | basic | HIGH | `memory compact save-summary` with populated DB |
| CR02 | Recover with project filter | basic | HIGH | `memory compact recover --project myproj` |
| CR03 | Recover without filter (all projects) | basic | MEDIUM | `memory compact recover` |
| CR04 | File-ops tracking in compact | adversarial | MEDIUM | Verify compact records file operations in journal |
| CR05 | Cross-project recovery leak | adversarial | CRITICAL | Recover for project A, verify no project B observations surface |

## Export Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| E01 | Obsidian export with project filter | basic | HIGH | `memory export obsidian --project myproj` |
| E02 | Dry-run export | basic | MEDIUM | `memory export obsidian --dry-run` |
| E03 | Type filter | basic | MEDIUM | `memory export obsidian --type bugfix` |
| E04 | Topic-key filter | basic | MEDIUM | `memory export obsidian --topic-key my-key` |
| E05 | Cross-project leaks in output | adversarial | CRITICAL | Export for project A, grep output for project B content |

## Workspace Subsystem

| ID | Scenario | Role | Severity if fails | Command pattern |
|----|----------|------|-------------------|-----------------|
| W01 | Create workspace with layout types | basic | HIGH | `memory workspace create myws --layout default` |
| W02 | Remove workspace without force (should fail if non-empty) | basic | MEDIUM | `memory workspace remove myws` |
| W03 | Remove workspace with force | basic | MEDIUM | `memory workspace remove myws --force` |
| W04 | Enter workspace | basic | MEDIUM | `memory workspace enter myws` |
| W05 | Detect current workspace | basic | LOW | `memory workspace detect` |
| W06 | Merge workspaces | basic | HIGH | `memory workspace merge source target` |
| W07 | Name with slashes or dots (L4 bug) | adversarial | HIGH | `memory workspace create "my/workspace.name"` |
| W08 | Hooks execution on workspace lifecycle | adversarial | MEDIUM | Verify hooks fire on create/enter/leave/remove |
