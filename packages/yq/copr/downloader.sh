#!/usr/bin/env bash

set -euxo pipefail

# Logging

function log-debug {
  if [ -n "${DEBUG:-}" ]; then
    echo 'debug:' "$@"
  fi
}

function log-info {
  echo 'info:' "$@"
}

function log-warn {
  echo 'warn:' "$@"
}

function log-error {
  echo 'error:' "$@"
}

function log-fatal {
  echo 'fatal:' "$@"
}

# Options and args parsing

TEMPLATE=''
STAGING_DIR=''

HELP='downloader.sh

    given a spec, download the sources which are URLs and generate a new spec with the downloaded filenames in place of the URLs.

USAGE:
    downloader.sh TEMPLATE [FLAGS] [OPTIONS]

PARAMETERS:
    TEMPLATE    The location of a template spec file. Required.

FLAGS:
    --help    Print this help and exit

OPTIONS:
    --staging-dir DIRECTORY   A directory to put downloads in - defaults to a temporary directory.
    --out DIRECTORY           A directory to write outputs to - defaults to .'

while [[ $# -gt 0 ]]; do
  case ${1} in
    --help)
      echo "${HELP}"
      exit 0
      ;;
    --staging-dir)
      STAGING_DIR="${2}"
      shift
      shift
      ;;
    --out)
      OUT="${2}"
      shift
      shift
      ;;
    -*)
      log-fatal "Unknown option: ${1}"
      exit 1
      ;;
    *)
      if [ -z "${TEMPLATE}" ]; then
        TEMPLATE="${1}"
        shift
      else
        log-fatal "Unknown argument: ${1}"
        exit 1
      fi
      ;;
  esac
done

if [ -z "${TEMPLATE}" ]; then
  log-fatal "TEMPLATE is required."
  exit 1
fi

if [ -z "${OUT:-}" ]; then
  OUT="$(pwd)"
fi

if [ ! -d "${STAGING_DIR}" ]; then
  STAGING_DIR="$(mktemp -d)"
fi

NAME="$(awk '/^ *Name: */ { print $2 }' "${TEMPLATE}")"
VERSION="$(awk '/^ *Version: */ { print $2 }' "${TEMPLATE}")"

DOWNLOADS_DIR="${STAGING_DIR}/${NAME}-${VERSION}"
SPEC="${OUT}/$(basename "${TEMPLATE}" | sed 's/.in$//')"
SOURCE="${OUT}/${NAME}-${VERSION}

mkdir -p "${DOWNLOADS_DIR}"

# Believe it or not, procedurally generating an awk script is the most
# straightforward way of staging the edits we want to make. 
script="$(mktemp)"

# For non-matches, just print the line. This regexp HAS to match the one used
# in the match loop, groups excepted.
# shellcheck disable=SC2016
echo '!/^ *Source[0-9]: *.*/ { print $0 }' > "${script}"

# Download the thing if it's a URL and print the filename
function download {
  local basename
  if [[ $url =~ (https?|ftp|file):// ]]; then
    basename="$(basename "${url}")"
    # TODO: --overwrite flag
    if [ ! -f "${DOWNLOADS_DIR}/${basename}" ]; then
      curl -L "${url}" -o "${DOWNLOADS_DIR}/${basename}" 1>&2
    fi
    echo "${basename}"
  else
    echo "${url}"
  fi
}

# we can use rpmspec -P to render the macros in yq.spec.in. Note that this
# means you can't get the original line number - nice try!
rpmspec -P yq.spec.in | awk 'match($0, /^( *Source([0-9]): *)(.*)/, groups) { print groups[1] "\t" groups[2] "\t" groups[3] }' | while read -r line; do
  set +x
  label="$(echo "${line}" | cut -d$'\t' -f1)"
  index="$(echo "${line}" | cut -d$'\t' -f2)"
  url="$(echo "${line}" | cut -d$'\t' -f3)"
  set -x

  src="$(download "${url}")"

  # We're SO CLOSE! We're trying to match on the same regexp but for the
  # index, but we're not capturing the index right now - we're capturing the
  # whole label!
  echo '/^ *Source'"${index}"': *.*/ { print "'"${label}"'" "'"${src}"'"}' >> "${script}"
done

log-info "--- running the following script in awk: ---"
while read -r line; do
  log-info "${line}"
done <<< "${script}"
log-info "--- end script ---"

awk -f "${script}" < "${TEMPLATE}" > "${OUT}"

rm "${script}"

(cd "${STAGING_DIR}" && tar -czf "${
