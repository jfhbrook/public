# omsxctl

omsxctl is a small rust cli console for controlling [openMSX](https://openmsx.org/)
over its socket API.

## install

you can install omsxctl with cargo:

```sh
cargo install omsxctl
```

I may offer builds and/or packages in the future - we'll see.

## use

first, start `openMSX` in the default socket ouput mode (in Linux/MacOS). then
fire up `omsxctl` and enjoy:

```
$ omsxctl

for available commands, visit: https://openmsx.org/manual/commands.html

openMSX> set power off
ok: false
openMSX> set power on
ok: true
openMSX> set power bananas
nok: can't set "power": expected boolean value but got "bananas"

openMSX>

$
```

if you do this on your own machine, you'll see that openMSX power cycles the
emulator.

## development

things are pretty informal. the program doesn't have a lot of surface area to
unit test - heck, the entire thing is in a single file right now. but otherwise
`cargo run` and friends work.

I don't see a *ton* of feature work on this project going forward. the biggest
missing feature in my mind is non-pretty output formats such as json or even
xml. if you want to take a crack at it, don't let me stop you!

## license

I'm putting this out there with an Apache 2.0 license. Read the LICENSE file
for more.
