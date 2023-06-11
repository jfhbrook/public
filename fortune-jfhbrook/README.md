# fortunes

this is a collection of quotes that I intend to use with fortune-mod.

## build

fortunes use both flat files to contain the actual quotes, and index files to
enable performant random access. to build the index files, you may run
`just` to trigger the buid step.

## install

you may install these by copying them to the directory your other fortunes are
in. on fedora this is `/usr/share/games/fortune`, but other systems have it
in `/usr/share/fortune` instead.

## COPR package

I have a .spec file which
[should work with COPR and tito](https://docs.fedoraproject.org/en-US/quick-docs/publish-rpm-on-copr/),
but I haven't done the work to get that package building yet. I just wanted to
get this data written down while it was on my mind!

## other TODOs

* remember and write down more good tweets
* refactor my old bash.org scraper to pull top 200 quotes

## license

*my* work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License [1]. that said, these are quotes collected from all sorts
of sources that I don't hold any copyright to, but which are - as far as I
know - fair use.

[1]. (to view a copy of this license, visit
<http://creativecommons.org/licenses/by-sa/4.0/> or send a letter to Creative
Commons, PO Box 1866, Mountain View, CA 94042, USA.)
