SHELL = /usr/bin/env bash

srpm:
	bash ./copr/srpm.sh

verify:
	rpmbuild --rebuild "$${outdir}/$$(basename "$${spec}" | sed 's/\.spec//')-"*.src.rpm && echo -e "\e[32msource rpm verified!\e[0m" || echo -e "\e[30msource rpm invalid!\e[0m"
