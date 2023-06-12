SHELL = /usr/bin/env bash

srpm:
	curl -L "https://github.com/mikefarh/yq/releases/download/v$$(cat "$${spec}"  | grep -E '^Version: ' | sed 's/^Version: //')/yq_linux_amd64.tar.gz" -o yq_linux_amd64.tar.gz
	rpmbuild --define "_topdir $$(pwd)" -bs "$${spec}"
	mv SRPMS/yq*.src.rpm "${{outdir}}/"
