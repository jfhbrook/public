# Packages!

These files configure some packages I'm building on COPR. This folder might
end up managing other registries as well, but for now it's just COPR.

Note that this folder only contains builds for packages I don't own. Individual
projects will have their own files for configuring COPR.

## COPR Project

You can look at a full list of my COPR packages here:

**<https://copr.fedorainfracloud.org/coprs/jfhbrook/joshiverse/packages/>**

## COPR `make srpm` builds

Some of these projects - such as `yq` - use COPR's `make srpm` builds. The entry
point for these builds, plus a bunch of supporting scripts, can be found in
[the .copr folder](../.copr).

Of particular interest will be the `download-sources` script, which downloads
source files based on the `Source[0-9]` entries in a `.spec.in` file.

## Templates

The [templates directory](./templates) contains some cookiecutter templates!
Try running `just new TEMPLATE_NAME` to generate a new package.

Note that there isn't a template for tito projects, since those are going to
be pretty custom. Consider copy-pasting out of `korbenware` or `coprctl`.
