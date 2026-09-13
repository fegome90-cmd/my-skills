{ config, pkgs, lib, ... }:
{
  programs.fish = {
    enable = true;
    generateCompletions = false; # Carapace or native bridges manage completions

    # PATH precedence lives in shellInit so NON-interactive shells
    # (`fish -c`, scripts) inherit it too.
    shellInit = ''
      # Structured PATH precedence:
      # local bins -> Nix profile -> (rest: Cargo/Bun -> Homebrew -> system)
      set -gx PATH $HOME/.local/bin $HOME/.local/state/nix/profiles/home-manager/home-path/bin $PATH
    '';

    interactiveShellInit = ''
      # Homebrew Environment (interactive only)
      if test -x /opt/homebrew/bin/brew
          eval (/opt/homebrew/bin/brew shellenv)
      end
    '';

    # Declare plugins directly; do NOT install fisher itself as a plugin
    # (fisher is a plugin manager, not a plugin). Resolve the real hash on
    # first build: run `nix build`, copy the `got:` hash from the error
    # output, and replace `lib.fakeHash`. Derivation-agnostic alternative:
    # `nix hash to-sri --type sha256 <path>`.
    # plugins = [
    #   {
    #     name = "tide";
    #     src = pkgs.fetchFromGitHub {
    #       owner = "IlanCosman";
    #       repo = "tide";
    #       rev = "v6.1.1";
    #       hash = lib.fakeHash;
    #     };
    #   }
    # ];
  };
}
