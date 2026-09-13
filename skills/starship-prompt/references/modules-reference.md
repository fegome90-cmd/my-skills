# Starship Modules Quick Reference

| Module | Purpose | Common Format / Settings |
| :--- | :--- | :--- |
| `os` | OS Logo / Distro Icon | `style = "bg:red fg:crust"`, `symbols = { Macos = "󰀵 ", Linux = "󰌽 " }` |
| `username` | User name & root indicator | `show_always = true`, `style_user = "bold blue"`, `style_root = "bold red"` |
| `hostname` | Machine host / SSH session | `ssh_only = true`, `format = "[$hostname]($style)"` |
| `directory` | Working directory & path | `truncation_length = 3`, `truncate_to_repo = true`, `substitutions = { "Developer" = "󰲋 " }` |
| `git_branch` | Current branch & remote | `symbol = " "`, `format = "[$symbol$branch]($style)"` |
| `git_status` | Working tree status & sync | `conflicted`, `ahead`, `behind`, `diverged`, `untracked`, `stashed`, `modified`, `staged`, `renamed`, `deleted` |
| `git_state` | Interactive rebase / merge state | Displays REBASING, MERGING, CHERRY-PICKING |
| `fill` | Dynamic spacing to push right | `symbol = " "` |
| `time` | Current system clock | `time_format = "%R"`, `disabled = false` |
| `cmd_duration` | Execution time of last command | `min_time = 500`, `show_milliseconds = true` |
| `character` | Prompt cursor / exit status | `success_symbol = "[❯](bold green)"`, `error_symbol = "[❯](bold red)"`, Vi-mode symbols (`vimcmd_*`) |
| `line_break` | Multi-line separator | Inserts newline `\n` cleanly between blocks |
| `status` | Numeric error exit code | `disabled = false`, `format = "[$status]($style)"` |

## Toolchain & Runtime Modules
* `nodejs`, `bun`, `deno`, `rust`, `golang`, `python`, `php`, `java`, `c`, `zig`, `kotlin`, `haskell`, `lua`, `ruby`, `elixir`, `package`.
* Common format pattern: `format = "[[ $symbol($version) ](fg:crust bg:green)]($style)"`.

## Cloud & Container Modules
* `docker_context`, `kubernetes`, `aws`, `gcloud`, `azure`, `terraform`, `conda`.
