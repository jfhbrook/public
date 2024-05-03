#!/usr/bin/env bash

VERSION="${1}"
PATCH="${2}"

SHA="$(sha256sum "korbenware-${VERSION}.tar.gz" | cut -d ' ' -f 1)"

FORMULA="$(exercise-bike ./templates/korbenware.rb.njk \
  --version "${VERSION}" \
  --patch "${PATCH}" \
  --sha "${SHA}")"

if [ -n "${HOMEBREW_TAP}" ]; then
  echo "$FORMULA" > "${HOMEBREW_TAP}/Formula/korbenware.rb"
  (cd "${HOMEBREW_TAP}" && git add "Formula/korbenware.rb")
  (cd "${HOMEBREW_TAP}" && git commit -m "korbenware v${VERSION}-${PATCH}")
  (cd "${HOMEBREW_TAP}" && git push)
else
  echo "To automatically commit and push the formula, set the HOMEBREW_TAP environment variable."
  echo ""
  echo "Generated formula:"
  echo ""
  echo "$FORMULA"
fi
