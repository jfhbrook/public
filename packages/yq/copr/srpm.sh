#!/usr/bin/env bash

set -euxo pipefail

source ../../.copr/bin/prelude.sh

download-sources
build-srpm
