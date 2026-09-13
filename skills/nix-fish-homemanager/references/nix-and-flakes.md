# Nix & Flakes Architecture on macOS

## 1. Flake Structure for Standalone Home Manager

In a standalone Home Manager setup on macOS (without `nix-darwin`), the root entrypoint is `flake.nix`.

```nix
{
  description = "Gentleman macOS Dotfiles & Home Manager Flake";

  # Pin rotation policy: `nixos-26.05` is supported until 2026-12-31.
  # Rotate before EOL: run `nix flake update` monthly and re-pin to the
  # next stable branch as the current one approaches EOL. Pins past
  # EOL stop receiving security patches.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/release-26.05";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, nixpkgs-unstable, home-manager, ... }@inputs:
    let
      mkHomeConfiguration = system:
        let
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };
          unstablePkgs = import nixpkgs-unstable {
            inherit system;
            config.allowUnfree = true;
          };
        in
        home-manager.lib.homeManagerConfiguration {
          inherit pkgs;
          modules = [
            ./fish.nix
            ./starship.nix
            # user-specific configuration
          ];
          extraSpecialArgs = { inherit inputs unstablePkgs; };
        };
    in
    {
      homeConfigurations = {
        "gentleman-macos-arm" = mkHomeConfiguration "aarch64-darwin";
        "gentleman" = mkHomeConfiguration "aarch64-darwin";
      };
    };
}
```

---

## 2. Flake Lifecycle & Core Commands

| Operation | Command | Effect | Safe for Dry-Run? |
| :--- | :--- | :--- | :--- |
| **Check Flake** | `nix flake check` | Evaluates flake inputs and typechecks expressions | Yes |
| **Clean Build** | `home-manager build --flake .#<profile>` | Generates `./result` derivation without touching `$HOME` | Yes (Recommended before switch) |
| **Build Activation** | `nix build .#homeConfigurations.<profile>.activationPackage` | Produces raw generation package in store | Yes |
| **Apply / Switch** | `home-manager switch --flake .#<profile>` | Activates new generation and updates profile symlinks in `$HOME` | Mutates active `$HOME` |
| **Update Lock** | `nix flake update` | Updates `flake.lock` with latest upstream commit hashes | Modifies `flake.lock` |
| **Garbage Collect** | `nix-collect-garbage --delete-older-than 30d` | Removes store derivations unreachable for >30 days | Caution: destroys old generations (rollback targets) |
| **Garbage Collect (aggressive)** | `nix-collect-garbage -d` | Removes ALL old generations, including rollback ability | NOT safe — destroys every rollback target |

---

## 3. Hermetic Evaluation & Store Immutability

* **World-Readable Store:** Everything referenced in `flake.nix` or imported Nix expressions is copied to `/nix/store/` with permissions `0444` (read-only for all local users).
* **Rule of Secrets:** NEVER interpolate secrets (`apiKey = "..."`, `ghp_...`) in Nix files or files copied via `home.file` or `home.activation`.
* **Git Tracked Requirement:** Nix Flakes only evaluate files that are tracked by Git (`git add`). Untracked files are invisible to the Nix evaluator.
