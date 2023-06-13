#!/usr/bin/env prm

# This is a test fixture! It also stands as an example. It's not in production
# use!

function apply {
  copr-set package-scm joshiverse korbenware \
    --type git \
    --method tito \
    --clone-url "https://github.com/jfhbrook/public" \
    --subdir "korbenware" \
    --spec "korbenware.spec" \
    --webhook-rebuild on
}

function status {
  copr-get package joshiverse korbenware
}
