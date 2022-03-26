{ pkgs ? import <nixpkgs> {
  overlays = [
    (import (builtins.fetchTarball
      "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"))
  ];
} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # cargo-watch
    ((rust-bin.fromRustupToolchainFile ./rust-toolchain.toml).override {
      extensions = [ "rust-src" ];
    })
    cargo-expand
    gcc
    cmake
    openssl
    zlib
    pkgconfig

    #python
    python38
    python38Packages.virtualenv

    # common
    watchexec
  ];
}
