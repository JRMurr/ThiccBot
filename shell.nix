{ pkgs ? import <nixpkgs> {
  overlays = [
    (import (builtins.fetchTarball
      "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"))
  ];
} }:
let
  basePackages = with pkgs; [
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

    nixfmt
  ];
  macInputs =
    (with pkgs.darwin.apple_sdk.frameworks; [ CoreFoundation CoreServices ]);
  inputs = basePackages
    ++ pkgs.lib.lists.optionals pkgs.stdenv.isDarwin macInputs;
in pkgs.mkShell {

  buildInputs = inputs;
}
