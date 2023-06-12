# TODO

## Now

- [X] implement options/command parsing
- [X] add --dry-run support
- [X] make default file stdin
- [X] implement 'get' command
  - a dumb thin wrapper that uses kubectl-like commands
  - support yaml output w/ yq if it's an easy lift
- [X] implement api-resources
- [X] implement config loading
- [X] get/save package-pypi (python-pyee)
- [X] make get/apply match for package-pypi
- [X] get/save package-scm (fortune-jfhbrook)
- [X] make get/apply match for package-scm
- [X] log in w/ copr-cli
- [X] test/fix apply for python-pyee
- [X] test/fix apply for fortune-jfhbrook
- [X] create a package-rubygems (t)
- [X] make get/apply match for package-rubygems
- [X] get/save/apply package-rubygems
- [X] add delete command (support -f)
- [ ] write real README
- [ ] make a tito-based COPR
- [ ] install via COPR

## Later

- [ ] implement config commands
  - currently can read from config file
  - but commands are not implemented, sadly
- [ ] make kinds capitalized
  - this is how k8s does it
  - but I have to do some mapping internally to support it
  - v1alpha2, anyone?
