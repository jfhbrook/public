#!/usr/bin/env bash

VERSION="${1}"
PATCH="${2}"

NOTES=''
TAKE_NOTES=''

while read line; do
  if [[ "${line}" == '%changelog' ]]; then
    TAKE_NOTES=1
  elif [ -n "${TAKE_NOTES}" ]; then
    if [ -z "${line}" ]; then
      break
    fi
    NOTES="${NOTES}
${line}"
  fi
done < korbenware.spec

gh release create "korbenware-${VERSION}-${PATCH}" \
  -t "korbenware v${VERSION}" \
  -n "${NOTES}" \
  "korbenware-${VERSION}.tar.gz"
