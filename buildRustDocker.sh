#!/usr/bin/env bash
set -e; set -o pipefail;

nix build '.#thiccBotDocker'
image=$((docker load < result) | sed -n '$s/^Loaded image: //p')
docker image tag "$image" thicc-bot:latest