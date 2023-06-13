# TODO

This is really close!! It almost works locally - but the behavior got me
confused and it's really particular. I need to:

- rename "staging" to "downloads"
- download a given source to ./downloads/0/${name}-${version}/whatever.filename
- (cd ./downloads/0/ && tar -xzf "${outdir}/${name}-${version}.tar.gz .)
- write out the name of the generated artifact instead of the original one

Then make sure the ol' `just test` works as expected. If that's healthy and
cleaned up, then give it a try on copr. If that works, then, uh...

Then I should

- move environment setup to .copr/bin/copr-prelude.sh
- move downloader.sh to .copr/bin/download-sources
- move the rpmbuild to .copr/bin/copr-srpm
- make the Makefile add those to the PATH when calling the project script
- move the project script to scripts/copr-srpm.sh

that will give my project one nice, neat script that reuses components shipped
for the project more generally, without making me ship them more broadly.

if I want to ship more broadly, I can have the makefile lazily dnf install its
deps.

I could also stand to decrease the size of the justfile. I can probably
delegate a lot of the environment overrides to automatic behavior in the
build script, and I probably want to move verification into the Makefile.
