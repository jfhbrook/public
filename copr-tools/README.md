# copr-tools

This repo packages a bunch of tools for working with Fedora RPMs and [COPR](https://copr.fedorainfracloud.org/) for Docker and MacOS. It contains the following:

- [`copr`](https://github.com/fedora-copr/copr)
- `copr-rpmbuild`
- `copr-tools` entry point for arbitrary commands in the Docker container
- [`coprctl`](../coprctl)
- `go2rpm`
- `pyp2spec`
- `rpmbuild`
- `rust2rpm`
- [`tito`](https://github.com/rpm-software-management/tito)

## Docker

The Docker image may be found here:

<https://hub.docker.com/repository/docker/jfhbrook/copr-tools/general>

It may be used to run tools like `coprctl`, as in this example:

```bash
exec docker run \
  -v "${HOME}:/root" \
  -v "$(pwd):/workspace" \
  -it "${COPR_TOOLS_IMAGE}:${COPR_TOOLS_VERSION}" coprctl "$@"
```

Note that `~` is being mounted under root's home, and that the current directory is being mounted under `/workspace`. The image is configured to treat `/workspace` as the current project, and most tools read configuration out of the container's uer home directly.

## Homebrew

I have a number of packages in [my Homebrew tap](https://github.com/jfhbrook/homebrew-joshiverse) which install shims that wrap this use of Docker for MacOS. They may be installed like so:

```bash
brew install jfhbrook/joshiverse/copr
brew install jfhbrook/joshiverse/copr-rpmbuild
brew install jfhbrook/joshiverse/copr-tools
brew install jfhbrook/joshiverse/coprctl
brew install jfhbrook/joshiverse/go2rpm
brew install jfhbrook/joshiverse/pyp2spec
brew install jfhbrook/joshiverse/rpmbuild
brew install jfhbrook/joshiverse/rust2rpm
brew install jfhbrook/joshiverse/tito
```

Note that Docker must be running in order for these scripts to work.

## Other Operating Systems

All of the Homebrew shims are implemented as Bash scripts in [the ./bin directory](./bin), and should work on any operating system supporting Docker and Bash.

## License

MIT/X11. See LICENSE for details.
