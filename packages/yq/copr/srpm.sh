#!/usr/bin/env bash

set -euxo pipefail

source ../../.copr/bin/prelude.sh

# TODO: download-sources should read everything it needs out of the environment
# TODO: download-sources should use the spec.in file if .spec doesn't exist,
# otherwise edit in-place - this will make these tasks somewhat composable
download-sources
build-srpm
