SHELL = /usr/bin/env bash

srpm:
	bash ./copr/srpm.sh

verify:
	rpmbuild --rebuild "${outdir}/$(basename "${spec}" | sed 's/\.spec//')-"*.src.rpm
