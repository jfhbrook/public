#!/usr/bin/env bash

source ../../.copr/bin/prelude.sh

set-gh-release-version mikefarah/yq
download-sources
build-srpm
