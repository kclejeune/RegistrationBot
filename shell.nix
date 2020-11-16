{ sources ? import ./nix/sources.nix }:
let
  pkgs = import sources.nixpkgs { };
  python-env = pkgs.python3.withPackages(ps: with ps; [
    selenium
    black
    pylint
  ]);
in pkgs.mkShell {
  buildInputs = with pkgs; [
    # keep this line if you use bash
    bashInteractive
    python-env
    geckodriver
    chromedriver
  ];
}
