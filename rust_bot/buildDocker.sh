#!/usr/bin/env bash

#https://nix.dev/tutorials/building-and-running-docker-images

docker load < $(nix-build hello-docker.nix)