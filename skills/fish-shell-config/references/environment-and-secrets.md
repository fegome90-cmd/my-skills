# Environment, PATH Layers, and Secrets — This Machine

Startup reality, in verified order:

1. `/etc/fish/config.fish` and `/etc/fish/conf.d/*` (system).
2. `hm-session-vars.fish` (home-manager session environment).
3. `~/.config/fish/conf.d/*.fish` — **lexical order, no numbering in use**. Tool hooks and secrets load here.
4. `~/.config/fish/config.fish` (home-manager symlink, runs LAST): managed aliases, `~/.nix-profile/bin`
   PATH prepend, `starship init fish | source`.

## PATH layers (who puts what)

| Layer | Adds |
|---|---|
| hm-session-vars | Nix/home-manager profile paths |
| `fish_user_paths` (universal) | `~/bin`, fnm node v24.18.0, `~/.npm-global/bin`, `codeium/windsurf/bin` |
| config.fish (managed) | `~/.nix-profile/bin` |
| conf.d hooks | direnv, nvm.fish may modify per-directory state |

Debug order: `echo $PATH`, `command -v node`, `node -v`. Remember two Node managers coexist
(nvm.fish plugin + fnm in `fish_user_paths`).

## Prompt and theme

- Prompt: **starship**, initialized from managed config.fish; binary lives in the home-manager Nix profile.
  Config changes go through starship's own config (deployed via Nix/Home Manager — see the
  `starship-nix-manager` skill), never through a `fish_prompt.fish`.
- Theme: catppuccin via `conf.d/plugin-catppuccin.fish`. `fish_frozen_theme.fish` /
  `fish_frozen_key_bindings.fish` are fish-4.3 migration files — do not edit.

## Plugins

fisher manages `jorgebucaran/fisher` and `jorgebucaran/nvm.fish` (`~/.config/fish/fish_plugins`).
Plugin internals live in `functions/` (`fisher.fish`, `nvm.fish`, `_nvm_*.fish`) — generated, do not hand-edit.

## The Keychain secret pattern (copy for new tools)

Verified pattern from `conf.d/claude-keychain.fish`. Store once:
`security add-generic-password -a "$USER" -s <service-name> -w <token> -U`
then create `conf.d/<tool>-keychain.fish`:

```fish
# Load <TOOL> secrets from macOS Keychain.
# On failure the variable stays UNSET (not empty) so the tool reports a clear
# "missing token" error instead of a confusing 401.

if test (uname) = Darwin
    set -l token (security find-generic-password -a "$USER" -s "<service-name>" -w)
    if test $status -eq 0
        set -x <TOOL>_TOKEN $token
    else
        echo "<tool>-keychain: Failed to load <TOOL>_TOKEN from Keychain" >&2
    end
end
```

Existing loaders: `claude-keychain` (ANTHROPIC_AUTH_TOKEN), `elevenlabs-keychain`, `openrouter`,
`aws-profile`, `cadsp`. Follow the same shape — Darwin guard, UNSET-on-failure, stderr message.

## conf.d inventory (what each file owns)

| File | Owns |
|---|---|
| `aws-profile.fish`, `cloud-profile.fish` | AWS/cloud profile selection |
| `api-keychain.fish`, `token-keychain.fish` | Keychain secret exports |
| `direnv.fish` | direnv hook (`type -q` guard) |
| `agent-env.fish`, `custom-env.fish` | agent tooling and workspace environment |
| `nvm.fish` | nvm.fish plugin hook |
| `project-launchers.fish` | project launcher aliases |
| `plugin-fisher.fish`, `plugin-catppuccin.fish` | plugin bootstrap |
| `fish_frozen_theme.fish`, `fish_frozen_key_bindings.fish` | fish 4.3 auto-generated (never edit) |

## Home-manager boundary

- `config.fish` is a symlink to `/nix/store/...-home-manager-files/...` — regenerated on every
  `home-manager switch`. Editing the store target is lost on next rebuild AND mutates the store.
- To change managed content (aliases, starship init, PATH): find the source flake/module. `home-manager
  generations` lists generations (store paths); grep the user's nix repos for `programs.fish` to find
  the defining module. Rebuild with the user's usual flake workflow — ask before running a switch.
- Rule of thumb: **interactive conveniences go in fish-editable surfaces; anything that must survive
  reinstalls goes in home-manager.**
