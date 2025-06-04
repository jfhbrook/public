#!/usr/bin/env bash

set -euo pipefail

VERSION="${1}"

SHA="$(sha256sum "copr-tools-${VERSION}.tar.gz" | cut -d ' ' -f 1)"

if [ -n "${HOMEBREW_TAP}" ]; then
  for template in ./templates/*.njk; do
    FORMULA="$(exercise-bike "${template}" \
      --version "${VERSION}" \
      --sha "${SHA}")"
    FILENAME="$(basename -s '.njk' "${template}")"

      echo "${FORMULA}" > "${HOMEBREW_TAP}/Formula/${FILENAME}"
      (cd "${HOMEBREW_TAP}" && git add "Formula/${FILENAME}")
  done

  (cd "${HOMEBREW_TAP}" && git commit -m "copr-tools v${VERSION}")
  (cd "${HOMEBREW_TAP}" && git push)
else
  echo "To automatically commit and push the formula, set the HOMEBREW_TAP environment variable."
fi
