#!/usr/bin/env bats

load "helpers.sh"

function setup {
  start-server
}

function teardown {
  stop-server
}

@test "basic auth" {
  RES="$(bbgurl -u 'josh:supersekritpw' "http://0.0.0.0:3000")"
  [ "$(get-header "${RES}" 'authorization')" = "Basic am9zaDpzdXBlcnNla3JpdHB3" ]
}
