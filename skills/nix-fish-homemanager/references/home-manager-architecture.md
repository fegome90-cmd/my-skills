# Home Manager Architecture on macOS

## 1. The Three Mechanisms for File & Program Management

Home Manager provides three tiers for configuring user environments:

### Tier 1: Canonical Native Modules (`programs.<name>`)
* **When to use:** Whenever Home Manager provides a built-in module (e.g. `programs.fish`, `programs.starship`, `programs.git`, `programs.gh`, `programs.zoxide`, `programs.atuin`).
* **Why:** Automatically manages binary packages in `home.packages`, generates optimized config files, and wires inter-module shell integrations (e.g. `programs.starship.enableFishIntegration`).
* **Example:**
  ```nix
  programs.starship = {
    enable = true;
    enableFishIntegration = true;
    settings = {
      palette = "catppuccin_mocha";
    };
  };
  ```

### Tier 2: Managed Declarative Symlinks (`home.file`)
* **When to use:** Dotfiles or configurations without a dedicated Home Manager module, or where exact raw files are checked into the repository (e.g. `zellij.nix`, `ghostty.nix`).
* **Mechanism:** Creates an immutable symlink from `$HOME/.config/<app>` to `/nix/store/<hash>-home-manager-files/...`.
* **Example:**
  ```nix
  home.file.".config/ghostty/config".source = ./ghostty/config;
  ```

### Tier 3: Activation Scripts (`home.activation.<name>`)
* **When to use:** Apps that require writable configuration directories (e.g. Zed, Neovim plugins, cache directories) or post-switch hooks.
* **Mechanism:** Shell script executed at the end of `home-manager switch`.
* **Pattern:** Always use `lib.hm.dag.entryAfter ["writeBoundary"] ''...''` and ensure idempotency.

---

## 2. macOS Profile Paths & Binary Precedence

In standalone Home Manager on macOS, generated binaries reside in:
* **Active Profile:** `~/.local/state/nix/profiles/home-manager/home-path/bin`
* **Legacy Profile Symlink:** `~/.nix-profile/bin`

To ensure Nix-managed binaries take precedence over system or Homebrew tools without breaking system utilities, order `$PATH` explicitly in your shell config:

`Pi / local bins` → `Nix profile` → `Cargo / Volta / Bun` → `Homebrew` → `/usr/bin`

---

## 3. The Declarative Plugin Pattern

Never run imperative plugin installers (`curl | source`, `fisher install <plugin>`, `tpm`) inside shell configuration files.
Declare plugins directly in Home Manager:

```nix
# Do NOT install fisher itself as a plugin — it is a plugin manager, not a
# plugin. Declare real plugins directly instead:
programs.fish.plugins = [
  {
    name = "tide";
    src = pkgs.fetchFromGitHub {
      owner = "IlanCosman";
      repo = "tide";
      rev = "v6.1.1";
      # Resolve on first build: `nix build` -> copy `got:` -> replace fakeHash.
      hash = lib.fakeHash;
    };
  }
];
```
Home Manager automatically places the plugin files in `~/.config/fish/conf.d/plugin-<name>.fish` and autoloads functions.
