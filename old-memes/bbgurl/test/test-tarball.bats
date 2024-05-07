#!/usr/bin/env bats

load "helpers.sh"

@test "tarball" {
  bbgurl http://nodejs.org/dist/v0.8.4/node-v0.8.4.tar.gz -o node-v0.8.4.tar.gz
  tar -xzf node-v0.8.4.tar.gz
  [ -d node-v0.8.4 ]
  rm -r node-v0.8.4
  rm node-v0.8.4.tar.gz
}
