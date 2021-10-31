{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    cargo-watch
    # rust stuff this might be overkill, copy pasted from elsewhere
    gcc
    cmake
    openssl
    zlib
    pkgconfig
    #python
    python39
    python39Packages.virtualenv
  ];
}
