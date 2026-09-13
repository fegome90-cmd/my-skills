# NOTE: this template references ./fish.nix and ./starship.nix, which are
# NOT included in the skill assets. Create them (or remove the entries from
# `modules`) before running `nix flake check`, otherwise evaluation fails.
{
  description = "Minimal Standalone Home Manager Flake for macOS";

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
      system = "aarch64-darwin";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
      unstablePkgs = import nixpkgs-unstable {
        inherit system;
        config.allowUnfree = true;
      };
    in
    {
      homeConfigurations."gentleman-macos-arm" = home-manager.lib.homeManagerConfiguration {
        inherit pkgs;
        modules = [
          ./fish.nix
          ./starship.nix
          # parenthesized lambda: destructured-arg lambdas need parens inside lists
          ({ lib, ... }: {
            home.username = lib.mkDefault "<username>";
            home.homeDirectory = lib.mkDefault "/Users/<username>";
            home.stateVersion = "26.05"; # set once at first install; never bump on channel rotation
            programs.home-manager.enable = true;
          })
        ];
        extraSpecialArgs = { inherit inputs unstablePkgs; };
      };
    };
}
