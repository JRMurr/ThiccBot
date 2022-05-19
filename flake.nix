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
        rustVersion =
          (pkgs.rust-bin.fromRustupToolchainFile ./rust-toolchain.toml);
        # pythonBackend = mach-nix.buildPythonPackage ./backend;
      in with pkgs; {
        packages = {
          thiccBotDocker = let
            platform = pkgs.makeRustPlatform {
              cargo = rustVersion;
              rustc = rustVersion;
            };
            thicc_bot = platform.buildRustPackage {
              pname = "thicc_bot";
              version = "0.1.0";
              src = ./rust_bot/.;
              cargoLock.lockFile = ./rust_bot/Cargo.lock;
            };
          in pkgs.dockerTools.buildImage {
            name = "thicc-bot";
            config = { Cmd = [ "${thicc_bot}/bin/thicc_bot" ]; };
          };
        };

        devShell = mkShell {
          buildInputs = [
            (rustVersion.override { extensions = [ "rust-src" ]; })

            cargo-expand
            gcc
            cmake
            # openssl
            zlib
            pkgconfig

            #python
            python38
            python38Packages.virtualenv
            # pythonBackend

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
