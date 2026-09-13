{ config, pkgs, lib, ... }:
{
  programs.starship = {
    enable = true;
    enableFishIntegration = true;
    enableZshIntegration = true;
    enableNushellIntegration = true;
    settings = {
      "$schema" = "https://starship.rs/config-schema.json";

      format = lib.concatStrings [
        "$directory"
        "$git_branch"
        "$git_status"
        "$fill"
        "$cmd_duration"
        "\n$character"
      ];

      add_newline = true;

      directory = {
        style = "bold blue";
        truncation_length = 3;
        truncate_to_repo = true;
      };

      git_branch = {
        style = "bold purple";
        symbol = " ";
      };

      character = {
        success_symbol = "[❯](bold green) ";
        error_symbol = "[❯](bold red) ";
      };
    };
  };
}
