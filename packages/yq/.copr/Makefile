SHELL = /usr/bin/env bash

srpm:
	mkdir -p "$$(pwd)/topdir/SOURCES"
	curl -L "https://github.com/mikefarh/yq/releases/download/v$$(cat "$${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')/yq_linux_amd64.tar.gz" -o "$$(pwd)/topdir/SOURCES/yq_linux_amd64.tar.gz"
	rpmbuild --define "_topdir $$(pwd)/topdir" -bs "$${spec}"
	mv "$$(pwd)/topdir/SRPMS/"yq*.src.rpm "$${outdir}/"
	rm -rf "$$(pwd)/topdir"
