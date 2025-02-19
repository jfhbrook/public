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
done < dbus-iface-markdown.spec

gh release create "dbus-iface-markdown-${VERSION}-${PATCH}" \
  -t "dbus-iface-markdown v${VERSION}" \
  -n "${NOTES}" \
  "dbus-iface-markdown-${VERSION}.tar.gz"
