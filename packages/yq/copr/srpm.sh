#!/usr/bin/env bash

set -euxo pipefail

source ../../.copr/bin/prelude.sh

echo "${PATH}"

download-sources
build-srpm
