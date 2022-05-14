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
              cargoSha256 =
                "15kiwpji3fg0mvzyj3d1hv1vcyzz8dfzl20752dhsjl4gzcm97a0";

              # use this when building new code, need a fake sha. Copy the real one from the error output
              # cargoSha256 = pkgs.lib.fakeSha256;
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
