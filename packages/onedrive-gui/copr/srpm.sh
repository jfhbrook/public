#!/usr/bin/env bash

source ../../.copr/bin/prelude.sh

set-gh-release-version bpozdena/OneDriveGUI
download-sources
build-srpm
