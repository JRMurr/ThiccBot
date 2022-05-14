{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs { inherit system overlays; };
        rustVersion = ((pkgs.rust-bin.fromRustupToolchainFile
          ./rust-toolchain.toml).override { extensions = [ "rust-src" ]; });
      in with pkgs; {
        devShell = mkShell {
          buildInputs = [
            rustVersion

            cargo-expand
            gcc
            cmake
            # openssl
            zlib
            pkgconfig

            #python
            python38
            python38Packages.virtualenv

            # common
            watchexec

            nixfmt
          ];

          shellHook = ''
            touch .env
          '';
        };
      });
}
