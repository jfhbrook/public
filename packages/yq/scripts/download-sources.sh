#!/usr/bin/env bash

set -euxo pipefail

# This script is started in the unpopulated source directory - download sources
# here, and they'll get tarballed appropriately by the parent.

curl -L "https://github.com/mikefarah/yq/releases/download/v${version}/yq_linux_amd64.tar.gz" | tar -xz
