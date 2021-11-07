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
  ];
}
