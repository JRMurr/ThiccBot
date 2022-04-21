let
  rustOverlay = (import (builtins.fetchTarball
    "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"));
  pkgs = import <nixpkgs> { overlays = [ rustOverlay ]; };
  rustSpecific =
    ((pkgs.rust-bin.fromRustupToolchainFile ../rust-toolchain.toml).override {
      extensions = [ "rust-src" ];
    });
  platform = pkgs.makeRustPlatform {
    cargo = rustSpecific;
    rustc = rustSpecific;
  };
  thicc_bot = platform.buildRustPackage {
    pname = "thicc_bot";
    version = "0.1.0";
    src = ./.;
    cargoSha256 = "15kiwpji3fg0mvzyj3d1hv1vcyzz8dfzl20752dhsjl4gzcm97a0";

    # use this when building new code, need a fake sha. Copy the real one from the error output
    # cargoSha256 = pkgs.lib.fakeSha256;
  };

in pkgs.dockerTools.buildImage {
  name = "thicc-bot";
  config = { Cmd = [ "${thicc_bot}/bin/thicc_bot" ]; };
}
