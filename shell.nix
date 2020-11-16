{ sources ? import ./nix/sources.nix }:
let
  pkgs = import sources.nixpkgs { };
  mach-nix = import sources.mach-nix { };
  python-env = mach-nix.mkPython {
    requirements = ''
      selenium==3.141.0
    '';
  };
in pkgs.mkShell {
  buildInputs = with pkgs; [
    # keep this line if you use bash
    bashInteractive
    python-env
    geckodriver
    chromedriver
  ];
}
