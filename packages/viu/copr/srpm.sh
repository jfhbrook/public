#!/usr/bin/env bash

source ../../.copr/bin/prelude.sh

set-gh-release-version atanunq/viu
download-sources
build-srpm
