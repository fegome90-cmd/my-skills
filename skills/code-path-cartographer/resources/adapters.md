# Adapters

Tool selection strategy. Pick the highest-priority adapter that works for the
current language and codebase state.

## Priority Chain

### 1. Trifecta Graph (Python — primary)

**Prerequisite:** `trifecta graph index` must have been run on the segment.

```bash
# Index (once per session or after code changes)
trifecta graph index --segment .

# Callers of a symbol
trifecta graph callers --symbol "func_name" --json

# Callees of a symbol
trifecta graph callees --symbol "func_name" --json
```

**When to use:** Python codebases with Trifecta installed and graph indexed.

**Limitation:** Python only (AST-based). If symbol not in graph, fall through.

### 2. Trifecta AST (Python — symbol extraction)

```bash
# Extract all symbols from a module
trifecta ast symbols "sym://python/mod|type/all"

# LSP hover for type info
trifecta ast hover --uri "file:///path/to/file.py:42:10"
```

**When to use:** Building symbol inventory for Python, getting type context.

### 3. ripgrep + git grep (All languages — backbone fallback)

Always available. Use for symbol discovery and reference counting.

```bash
# Find symbol definitions
rg "^(def |class |func |export )(TARGET)" --type <lang>

# Find all references
rg "TARGET" --type <lang> -n

# Find imports
rg "import TARGET|from .* import TARGET" --type <lang>

# Cross-file reference search
git grep "TARGET" -- <path>
```

**Language hints for entrypoint detection:**

| Extension | Entrypoint patterns |
|-----------|-------------------|
| `.go` | `func main()`, `package main` |
| `.py` | `if __name__`, `@app.route`, `click`, `argparse` |
| `.ts`/`.js` | `export default`, `app.get/post`, `router.` |
| `.sh` | Any executable shell script |
| `.rs` | `fn main()` |

### 4. Trifecta ctx_search (All languages — semantic boost)

```bash
trifecta ctx_search "authentication middleware" --k 10
```

**When to use:** When rg misses references due to renaming, aliasing, or
conceptual relationships. Semantic search catches what grep cannot.

**Do NOT use as primary adapter.** It returns ranked chunks, not structured
call graphs. Use to supplement rg findings.

### 5. Neovim Headless (LSP — optional, last resort)

```bash
nvim --headless -c "lua vim.lsp.buf.references()" -c "q" file.py
```

**When to use:** Language has LSP server available, rg is insufficient,
and Trifecta graph doesn't cover the language.

**Requires:** Language server installed for the target language.

**Note:** Slow and fragile. Only use when other adapters fail.

## Adapter Selection Logic

```
detect_language(files)
if language == "python" AND trifecta_available AND graph_indexed:
    adapter = TRIFECTA_GRAPH
else:
    adapter = RG_GREP

# Boost with semantic search
if trifecta_ctx_available AND confidence < HIGH:
    boost = TRIFECTA_CTX_SEARCH
```

## Adapter Health Check

Before starting, verify adapter availability:

```bash
# Trifecta
command -v trifecta && trifecta graph status --segment . 2>/dev/null

# ripgrep
command -v rg

# git grep (inside git repo)
git rev-parse --is-inside-work-tree 2>/dev/null
```
