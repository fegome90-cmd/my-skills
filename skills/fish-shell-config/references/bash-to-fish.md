# Bash → Fish Migration Reference

Condensed translation for porting bash habits. Fish never word-splits and all variables are lists —
most bash quoting/looping patterns collapse.

## Translation table

| Bash | Fish | Note |
|---|---|---|
| `VAR=value` | `set VAR value` | |
| `export VAR=value` | `set -gx VAR value` | global + exported |
| `VAR=$(cmd)` | `set VAR (cmd)` | splits on **newlines only** → list |
| `$?` | `$status` | |
| `$@` / `$1` | `$argv` / `$argv[1]` | lists are 1-indexed |
| `${VAR}` | `$VAR` or `{$VAR}VAR` | braces only for adjacency |
| `$((1+2))` | `math 1 + 2` | or `(math $x + 1)` |
| `[[ ... ]]` | `test ...` | also `[ ... ]` |
| `cmd1 && cmd2` | `cmd1; and cmd2` | `||` → `; or` |
| `for i in {1..10}` | `for i in (seq 1 10)` | |
| `$(ls)` split on spaces | `(ls)` split on newlines | each entry one list element |
| `VAR=${VAR:-x}` | `set -q VAR; or set VAR x` | |
| subshell `( ... )` | `begin; ...; end` | grouping only, same scope |
| heredoc `<<EOF` | `echo`/files/`printf` | no heredocs in fish |
| `until` | `while not test ...` | no `until` |

## Variables and scope flags

- `-l` local block/function · `-g` global session · `-U` universal (persists across sessions, stored in
  `fish_variables`) · `-x` exported to children. Combine: `-gx`, `-Ux`.
- **Scope gotcha (verified):** top-level `set -l` in a script is invisible inside functions it calls.
- PATH is a list: `set -gx PATH ~/bin $PATH`; prepend/append with `set -p` / `set -a`.
- Persistent PATH on this machine: `set -U fish_user_paths ~/dir $fish_user_paths` (fish prepends it).

## Lists

```fish
set items one two three
count $items            # 3
$items[1]               # one   (1-indexed)
$items[-1]              # three (last)
$items[2..-1]           # two three
set -a items four       # append
set -p items zero       # prepend
for item in $items; echo $item; end   # safe: no word splitting ever
```

## Strings (the `string` builtin)

```fish
string split ':' "a:b:c"          # a b c (list)
string join ',' a b c             # a,b,c
string replace -a 'old' 'new' $v  # replace all
string match -q '*pat*' $v        # exit status; use with `; and`
string length "hello"             # 5
string upper / string lower
string trim $v
```

## Control flow

```fish
if test -e $file
    ...
else if test $count -gt 5
    ...
end

switch $argv[1]
    case start
    case stop
    case '*'
        echo "unknown" >&2
        return 1
end

while test $count -lt 10
    set count (math $count + 1)
end
```

## Quoting

- Single quotes: literal, no expansion. Double quotes: variables and `(...)`/`(...)` expand, **no word splitting**.
- `"$var"` and `$var` are identical — quote only to glue text (`"prefix$var"`).
- Apostrophes inside single-quoted descriptions: `--description '... agent\'s ...'` is valid and
  `fish_indent`-clean, but keep descriptions on one line.

## Common ports seen on this machine

- Wrapper forcing a flag: `tmux.fish` → `function tmux; command tmux -2 $argv; end`
- Launcher alias to a repo CLI: `trifecta.fish` → `uv --directory <repo> run trifecta $argv`
- Conditional-then-launch with captured log + exit-status check: see `functions/piup.fish` (the reference
  implementation of guard + log + branch + prompt-handoff).
