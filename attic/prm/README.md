# prm
## "but who will manage the package managers?"

## NOTICE: prm is deprecated!

`prm` has been replaced with [coprctl](https://github.com/jfhbrook/public/tree/main/coprctl),
which leverages ideas developed in this project but uses yaml to manage a
kubectl-like DSL instead.

## hello

`prm` is a semi-[declarative](https://en.wikipedia.org/wiki/Declarative_programming) [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) on top of an unholy combination of
javascript and bash, with a particular focus on managing package registries.
it currently only works - to an extent, anyway -
with [COPR](https://copr.fedorainfracloud.org). in will likely support
other registries in the future, such as [npm](https://npmjs.org),
[PPA](https://launchpad.net/ubuntu/+ppas) or
[homebrew taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap), as I
find an interest in packaging on those platforms.

## confused? let's go over an example

I have [a project called korbenware](https://github.com/jfhbrook/public/tree/main/korbenware),
which has a Fedora spec file. I use [tito](https://github.com/rpm-software-management/tito)
to manage doing this with git. you can see the spec file [here]()https://github.com/jfhbrook/public/blob/main/korbenware/korbenware.spec.

I'm also building this project on COPR. COPR has a
[simple but serviceable cli](https://developer.fedoraproject.org/deployment/copr/copr-cli.html)
that can be used to execute CRUD operations for you. we can use this tool to
configure COPR from the command line.

what we "really want" is a declarative language similar to [terraform](https://www.terraform.io/)
which takes a specification for what you want resources to look like, diffs that
specification with the environment, and applies the changes on an as-needed basis.
but what life gives us is cli tools, not go libraries - and in COPR's case you
don't even get upserts.

enter `prm`. In my homelab infrastructure files, I have a bash script at
`packages/korbenware/prm.sh` that looks like this:

```bash
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
```

then I can upset that package spec using `prm`:

```bash
$ prm apply --verbose --copr-only
debug:    _ __  _ __ _ __ ___  
debug:   | '_ \| '__| '_ ` _ \ 
debug:   | |_) | |  | | | | | |
debug:   | .__/|_|  |_| |_| |_|
debug:   |_| "but who will manage
debug:        the package managers?"
debug:   
debug:   it worked if it ends with ok
debug:   FEATURE_COPR=activated
debug:   FEATURE_NPM=activated
debug:   HELP=deactivated
debug:   PRETEND=deactivated
debug:   PLZKTHX=deactivated
debug:   SHRUG=deactivated
debug:   DEBUG=activated
debug:   QUIET=deactivated
debug:   running command:
debug:   #!/usr/bin/env prm
debug:   
debug:   function apply {
debug:     copr-set package-scm joshiverse korbenware \
debug:       --type git \
debug:       --method tito \
debug:       --clone-url "https://github.com/jfhbrook/public" \
debug:       --subdir "korbenware" \
debug:       --spec "korbenware.spec" \
debug:       --webhook-rebuild on
debug:   }
debug:   
debug:   function status {
debug:     copr-get package joshiverse korbenware
debug:   }
debug:   
debug:   
debug:   apply
info:     LEROY JENKINS! 
Create or edit operation was successful.
info:    apply exited with code 0
info:    ok
```

and check the status as well:

```bash
$ prm status
info:     LEROY JENKINS! 
{
  "auto_rebuild": true,
  "id": 870660,
  "latest_build": null,
  "latest_succeeded_build": null,
  "name": "korbenware",
  "ownername": "jfhbrook",
  "projectname": "joshiverse",
  "source_dict": {
    "clone_url": "https://github.com/jfhbrook/public",
    "committish": "",
    "source_build_method": "tito",
    "spec": "korbenware.spec",
    "subdirectory": "korbenware",
    "type": "git"
  },
  "source_type": "scm"
}
info:    status exited with code 0
info:    ok
```

this tool does absolutely unspeakable things to make this work, but it *does*
give us that declarative feel we crave while also using the cli tools to do
the heavy lifting. I'm currently using this - or trying to anyway, making
robust specs is hard - for multiple COPR builds, and it works *reasonably* well.

## installation

prm is [distributed through npm](https://npm.im/@jfhbrook/prm). the examples
show using it as though it were globally installed with `npm i @jfhbrook/prm -g`,
but it will work just as well with a run-script strategy or via npx.

## development

honestly, if you try to use this and you're not Josh H, you got chutzpah. but
basically all I'm doing is pointing it at my COPR (or other registries) and
trying to do stuff with it. that aside: `bin/prm` is where the bulk of the
javascript logic is, and `actions` is where the bulk of the bash logic is. my
development loop is basically to edit live until the thing I want to do in
COPR works, then run prm for everything I have configured to make sure nothing
exploded.

## license

`prm` is distributed under an Apache 2.0 license.
