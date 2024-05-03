#!/usr/bin/env bash

source ../../.copr/bin/prelude.sh

set-gh-release-version bpozdena/OneDriveGUI 'v1.0.3'
download-sources
build-srpm
