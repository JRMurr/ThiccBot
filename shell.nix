{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # rust stuff
    gcc
    cmake
    openssl
    zlib
    pkgconfig
    postgresql_12
    #python
    python39
    python39Packages.virtualenv
  ];
}
