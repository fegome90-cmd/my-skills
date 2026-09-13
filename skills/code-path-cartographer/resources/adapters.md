# Adapters

Tool selection strategy. Pick the highest-priority adapter that works for the
current language and codebase state, prioritizing universal tools over proprietary ones.

## Priority Chain

### 1. ripgrep + git grep (Universal Primary — All Languages)

Always available, fast, and multi-language. Use for symbol discovery, caller/callee tracing, and reference counting across repositories.

```bash
# Find symbol definitions
rg "^(def |class |func |export )(TARGET)" --type <lang>

# Find all references (callers / consumers)
rg "\bTARGET\b" --type <lang> -n

# Find imports
rg "import TARGET|from .* import TARGET" --type <lang>

# Cross-file reference search with git
git grep "\bTARGET\b" -- <path>
```

**Language hints for entrypoint detection:**

| Extension | Entrypoint patterns |
|-----------|-------------------|
| `.go` | `func main()`, `package main` |
| `.py` | `if __name__`, `@app.route`, `click`, `argparse`, `typer` |
| `.ts`/`.js` | `export default`, `app.get/post`, `router.`, `main()` |
| `.sh` | Any executable shell script, `main "$@"` |
| `.rs` | `fn main()` |

### 2. Language-Native AST & Parsers (High-Precision Syntax Trace)

When regex patterns are ambiguous due to symbol shadowing, method overloading, or deep scope nesting, use the language's native AST parser or standard CLI tools.

```bash
# Python: inspect AST directly with standard library
python3 -c "import ast, sys; tree=ast.parse(open('file.py').read()); print([n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))])"

# TypeScript / JavaScript: extract AST / types via compiler or tree-sitter
npx tsc --noEmit
# or tree-sitter CLI if installed
tree-sitter parse file.ts 2>/dev/null

# Go: inspect package AST and symbols
go doc -all ./...
```

**When to use:** Resolving precise caller/callee signatures, module boundaries, and type references without false regex matches.

### 3. Language Server Protocol / Symbol Indexers (LSP)

In development environments with an active language server (e.g. `pyright`, `gopls`, `tsserver`, `rust-analyzer`), query symbol definitions and workspace references.

```bash
# Querying references via workspace language servers
# Provides compiler-verified symbol reachability and rename-safe references
```

**When to use:** Complex enterprise repositories with heavy indirection, interface implementations, and cross-package dependency graphs.

### 4. Optional Graph Engines & MCP Tools (Opt-in Accelerators)

If the workspace has graph-aware indexing tools (such as `graphify` MCP, `ctags`, or local code-graph CLI utilities):

```bash
# Use graph tools to supplement BFS/DFS traversals when available
```

**Rule:** Graph engines are optional accelerators. A missing graph engine MUST NEVER block or fail the cartography procedure; always fallback cleanly to `rg` + native AST.

## Adapter Selection Logic

```text
detect_language(files)

if language_parser_available(language):
    primary_adapter = RG_PLUS_NATIVE_AST
else:
    primary_adapter = RG_GREP

if graph_tool_available():
    booster = GRAPH_ACCELERATOR
else:
    booster = NONE
```

## Adapter Health Check

Before starting, verify tool availability:

```bash
# ripgrep (required)
command -v rg

# git grep (inside git repo)
git rev-parse --is-inside-work-tree 2>/dev/null

# Python runtime (if target is Python)
command -v python3

# Node / TypeScript runtime (if target is TS/JS)
command -v node
```
