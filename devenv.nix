{
  pkgs,
  lib,
  config,
  ...
}:
{
  languages.python = {
    enable = true;
    version = "3.13";
    uv = {
      enable = true;
      sync.enable = true;
    };
  };
}
