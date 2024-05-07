#!/usr/bin/env bats

load "helpers.sh"

function setup {
  start-server
}

function teardown {
  stop-server
}

@test "headers" {
  RES="$(bbgurl "http://0.0.0.0:3000" -H '{"Content-Type": "application/json"}')"
  [ "$(get-header "${RES}" 'content-type')" = "application/json" ]
}
