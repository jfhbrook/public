#!/usr/bin/env bash

source ../../.copr/bin/prelude.sh

set-gh-release-version starship/starship
download-sources
build-srpm
