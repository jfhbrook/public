# TODO

So at this point, I more or less have things shaped the way I want them, up
to where I call `download-sources`. But I need to catch up there!

There are two really big issues with `download-sources`. The first is that
it's currently scripted as being driven by args, when everything else reads
its configuration from the environment. So I need to make it read everything it
needs from there. If there's a tunable not exposed, expose it as an env var and
set that env var in prelude.sh. If it needs to be set to something to work
locally, do it in the justfile. Eventually this should get to the point where
it can't cd into a directory after unpacking a source, during `just test`.

The second is that the behavior for bundling a source is currently wrong, which
causes the error about cd-ing into a directory after unpacking a source. It
turns out nailing down this behavior is hard! But I did the research. We
need to do this instead:

- rename "staging" to "downloads"
- download a given source to ./downloads/0/${name}-${version}/whatever.filename
- (cd ./downloads/0/ && tar -xzf "${outdir}/${name}-${version}.tar.gz .)
- write out the name of the generated artifact instead of the original one

This should make `just test` work end-to-end locally. At that point, it's time
to see what COPR will do with it! If *that* works, then we're done - and what
will we have?

We'll have the framework for building a little DSL for doing up `make srpm`
based COPR builds in the public repo. If that works and I wanna use it for
other repos, I can always turn it into a template or something!
