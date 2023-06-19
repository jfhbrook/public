# coprctl

`coprctl` is a thin wrapper around [copr-cli](https://developer.fedoraproject.org/deployment/copr/copr-cli.html)
which implements a `coprctl apply` command, inspired by [kubectl](https://kubernetes.io/docs/reference/kubectl/)
and leveraging [yq](https://github.com/mikefarah/yq).

## Install

It's a portable bash script, but also I'm working on getting it up in my
personal COPR.

## Config

You'll need to create a config file at `~/.config/coprctl/config.yml`. Someday
I'll add commands to `coprctl` to initialize and manage the config - but for
today, my config is in [./example/config.yml](./example/config.yml).

## Usage

The basics are:

```bash
coprctl apply -f ./copr.yml
```

where `copr.yml` has a list of resources. For example:

```yaml
---
apiVersion: coprctl/v1alpha1
kind: project
metadata:
  name: "do-not-delete-me-2"
spec:
  description: "a test COPR"
---
apiVersion: coprctl/v1alpha1
kind: package-pypi
metadata:
  name: "python3-pyee"
spec:
  projectname: "do-not-delete-me-2"
  specGenerator: "pyp2spec"
  pythonversions:
    - "3"
---
apiVersion: coprctl/v1alpha1
kind: package-rubygems
metadata:
  name: "rubygem-t"
spec:
  projectname: "do-not-delete-me-2"
  gem: "t"
```

The commands have mostly-right documentation with the `--help` flag. Another
example of this format can be seen at
[./example/resources.yml](./example/resources.yml).

## File Format

I did my best to make properties match the options in the CLI. They aren't the
same as the ones in the API responses, but this way you can look at the help
for `copr-cli` as a guide for what the properties should be.

Kinds are lowercase. This is **not** how Kubernetes does it - they distinguish
between a lowercase type and a pascal-case Kind, but COPR doesn't do that at
all, and this way it's less mapping.

## Status

This project is a proof-of-concept that I wrote over a weekend to scratch my
very specific itches. Many/most package types are unimplemented (though
adding them is easy and I'll do so as I need them).

Moreover, limitations of `copr-cli` make implementing get/apply for all
resources very challenging! For instance, projects don't have a `get` because
the response format isn't in JSON or YAML - possibly it's a format useful
to `dnf`?

Finally, I haven't implemented config commands at *all*. This is just a matter
of me being lazy - it's definitely doable!

## Future

I plan on using this project as-is for my own needs. However, long term I think
the right answer might be to add this sort of functionality directly to
`copr-cli`. I made an issue here:

**<https://github.com/fedora-copr/copr/issues/2767>**

## License

MIT/X11. See LICENSE for details.
