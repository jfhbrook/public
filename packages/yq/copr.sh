#!/usr/bin/env bash

rpmbuild --define "_rpmdir ${outdir}" -bs "${spec}"
