# Authoring and Testing Fish Functions

Read this before writing any function file on this machine. It carries the template, the guards,
and the mandatory validation workflow.

## Function template

```fish
function name --description 'One line, shown in completions'
    # Guard: argument count
    if test (count $argv) -eq 0
        echo "Usage: name <arg>" >&2
        return 1
    end

    # Guard: external dependency
    if not type -q jq
        echo "name: jq is required. Install with: brew install jq" >&2
        return 1
    end

    set -l result (command that might fail)
    if test $status -ne 0
        echo "name: failed" >&2
        return 1
    end

    echo $result
end
```

Rules:

- One function per file at `~/.config/fish/functions/name.fish` — the filename IS the autoload key.
- `--description` is required for anything non-trivial (shows in completions). Keep it on ONE line:
  a wrapped/mis-formatted description line fails `fish_indent --check`.
- Use `--wraps 'original command'` to inherit completions when wrapping a command (see `tmux.fish`).
- Use `--argument-names a b` for named positional args; validate with `count $argv`.
- Error paths write to **stderr** (`>&2`) and `return 1`. Never echo errors to stdout.
- Shadow the wrapped binary with `command tmux $argv` inside wrappers, never a bare recursive call.

## Event handlers (occasionally useful)

```fish
function __on_pwd_change --on-variable PWD
    # runs on every cd
end
function __on_exit --on-event fish_exit
    # runs at shell exit
end
```

## Editing an existing function interactively

`funced name` opens it in `$EDITOR`; `funcsave name` persists it to `functions/`. Prefer writing the file
directly when the change is scripted — funced/funcsave is for quick interactive iteration.

## Validation gates (run ALL of them, in order)

```bash
fish -n <file>                        # 1. syntax
fish_indent -w <file>                 # 2. auto-format in place
fish_indent --check <file>            # 3. must exit 0 (pi-lens enforces this on edits)
fish -c 'source <file>; functions <name>'   # 4. loads and defines
```

## Stub-test pattern (behavior gate)

For any function with branches, test the branches with a stub harness — proven on `piup`:

```fish
#!/usr/bin/env fish
# /tmp/test_<name>.fish — scenario harness. Run: fish /tmp/test_<name>.fish <scenario>
set -g scenario $argv[1]   # NOT set -l! (see gotcha below)

function somecommand       # stub the externals the function calls
    echo "stub output"
    if test "$scenario" = error
        echo "✖ simulated failure" >&2
        return 1
    end
    return 0
end

source ~/.config/fish/functions/<name>.fish
<name>            # exercise the branch for $scenario
```

Run it once per scenario (`fish /tmp/test_name.fish clean`, `... error`) and assert each branch behaves.
Keep the harness in `/tmp` — it is disposable.

**The gotcha this pattern exists for:** a `set -l` at the top level of a script is invisible inside
functions the script calls (functions see their own local scope, not the script's). Verified on this
machine: a stub reading a top-level `set -l scenario` got an empty list. Always `set -g` (or `set -gx`)
in harnesses.

## Debugging

- `fish -d 3 -c 'command'` — debug output.
- `type name` — shows how a name resolves (function/alias/binary + definition).
- `functions name` — prints the loaded function body.
- `set -S VAR` — shows a variable with scope details.
- Echo markers beat theorizing: when in doubt, `echo "point X: var=($var)" >&2` and run the scenario.
