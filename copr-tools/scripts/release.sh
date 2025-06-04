#!/usr/bin/env bash

VERSION="${1}"

gh release create "copr-tools-${VERSION}" \
  -t "copr-tools v${VERSION}" \
  "copr-tools-${VERSION}.tar.gz"
