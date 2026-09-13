# Wiki Maintenance Anti-Patterns

Common pitfalls extracted from real wiki-keeping sessions. Learn from these mistakes.

## A1: Trusting Lint Numbers Without Spot-Check

**Symptom:** Report "27 orphans, 43 broken refs" as facts. After investigation, 98% were false positives.
**Root cause:** Detection scripts assumed one format but wiki used another.
**Fix:** Lint output is hypothesis, not diagnosis. Always spot-check 5 random findings before reporting or fixing.

## A2: Passing Pre-Processed Content to Sub-Agents

**Symptom:** Summarized source material into the task prompt. Sub-agent wrote summaries instead of real content.
**Root cause:** Sub-agents can't produce accurate output from digested inputs.
**Fix:** Pass raw content or give URLs directly. Never summarize what they need to read.

## A3: Fixing Wiki Debt Before Fixing Lint Script

**Symptom:** Tried to fix "orphans" by adding cross-refs. Real problem: detection script didn't understand path-based refs.
**Root cause:** If the test is buggy, fixing the "failures" makes things worse.
**Fix:** Always verify lint script correctness against known-good wiki state before running fixes. Fix the script first.

## A4: Single-Format Assumption in Cross-Ref Detection

**Symptom:** Script checked `[[basename]]` only. Wiki used `[[systems/tmux-fork]]`, `[[patterns/handoff-builder]]`, etc.
**Root cause:** Cross-ref formats vary; detection must handle all valid formats.
**Fix:** Lint scripts must handle both `[[basename]]` and `[[path/basename]]` formats. Read WIKI-SCHEMA for valid ref conventions.

## A5: Reporting Without Classification

**Symptom:** "43 broken refs" mixed template placeholders, external refs, and real broken links into one number.
**Root cause:** Aggregated numbers hide signal.
**Fix:** Classify every finding as `SCRIPT_BUG | TEMPLATE_PLACEHOLDER | REAL_DEBT` before reporting. See lint-checklist.md.

## A6: Timeout Without Partial Results

**Symptom:** Long task timed out. All work lost because sub-agent buffered everything for a final write.
**Root cause:** No incremental output strategy.
**Fix:** In spawn tasks, specify "write results to disk as you go, don't buffer everything."

---

**Remember:** The two-phase lint workflow (detect → classify → validate → fix → verify) exists specifically to prevent A1, A3, A4, and A5.

## A7: Sub-Agent Timeout on Large Ingests

**Symptom:** Sub-agent completes in 19s with 0 tokens, reporting "Now let me read all the source docs" as its final output.
**Root cause:** Sub-agent timed out or hit context limits before actually reading files. Large ingests (65+ files, 12k+ lines) need more time and explicit file-by-file instructions.
**Fix:** Set `runTimeoutSeconds ≥ 900` for large ingests. List every file path explicitly in the task. Prioritize read order. Tell the agent to write each page to disk immediately, not buffer.

## A8: Lint False Positives from Short-Form Refs

**Symptom:** Lint reports 40+ "broken refs" and "orphans" that are actually valid wiki-style `[[basename]]` links to `[[path/basename]].md`.
**Root cause:** Lint scripts only checked exact filename match, not basename resolution. Wiki refs support both `[[page]]` and `[[dir/page]]` formats.
**Fix:** Use `grep -r "\[\[.*${basename}.*\]\]\]"` for orphan detection (basename-aware). Use `basename=$(basename "$target")` + `find -name "${basename}.md"` for broken ref detection. Add all short-form refs to `excluded_refs:` in WIKI-SCHEMA.

## A9: Index Not Updated by Sub-Agent

**Symptom:** Sub-agent creates pages but index.md is empty or incomplete.
**Root cause:** Sub-agent ran out of context/time before reaching the "update index" step.
**Fix:** Always verify index completeness after sub-agent completion. Run the missing-from-index check immediately. If pages are missing, update index manually.
