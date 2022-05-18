#!/usr/bin/env bash

set -euo pipefail


function test-start {
  echo "test suite: $1"
  echo "--------------------------"
  PASSED=0
  FAILED=0
  PLANNED="${2:-}"
}

function assert-eq {
  local name="$1"
  local expected="$2"
  local message="${3:-}"

  eval "local actual=\$${name}"

  if [ -z "$message" ]; then
    message="\$${name}='${expected}'"
  fi

  if [ "${actual}" == "${expected}" ]; then
    echo "✅ ${message}"
    ((PASSED=PASSED+1))
  else
    echo "❌ ${message} (actual: '${actual}')"
    ((FAILED=FAILED+1))
  fi
}

function assert-true {
  assert-eq $1 1
}

function assert-false {
  assert-eq $1 ''
}

function test-finish {
  if [ -n "${PLANNED}" ]; then
    local total=$((PASSED+FAILED))
    assert-eq total "${PLANNED}" "ran ${PLANNED}/${total} tests"
  fi
  echo "-----------------"
  echo "passed: ${PASSED}"
  if [ "${FAILED}" -gt 0 ]; then
    echo "FAILED: ${failed}"
    echo "NOT OK"
    exit 1
  else
    echo "OK"
    exit 0
  fi
}


eval "$(./primitivist -B foo -B bar -S baz -- --foo --baz quux a b c)"

test-start 'primitivist tests'

assert-false HELP
assert-true FOO
assert-false BAR
assert-eq BAZ quux

test-finish
