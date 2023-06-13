# attic

Retired projects.

## alacritty-theme-tester

Some scripts I used to test alacritty themes. Very hacky! I also don't use
alacritty.

## college

Some code from when I was in college.

### lolcode

One of those projects was a fork of a `lolcode` interpreter which added some
advanced functions.

**<https://github.com/jfhbrook/lolcode>**

### db_hooks

This is the toolset I made for myself to manage database stuff on my personal
machines. It's currently not in use as it hasn't kept up with my tooling, but
will probably be dusted off in the future. It is licensed under an Apache v2.0
license.

## ecstatic

A static fileserver module for Node.js that I wrote in 2011. 

**<https://github.com/jfhbrook/node-ecstatic>**

I stopped maintaining it in 2019. You can read about why here:

<https://github.com/jfhbrook/node-ecstatic/issues/259>

I have dreams of rewriting it in typescript, but it turns out that's a tall
order.

## ias

PDF reports on course evaluations from when I was in college. It contains
2006 through 2009. Unfortunately, they're not even slightly scrapeable and I
didn't end up doing anything interesting with them.

## ihydra

**<https://github.com/jfhbrook/ihydra>**

A Jupyter kernel for the [hydra](https://hydra.ojack.xyz) live-coding video
synth. I hacked this up based on ijavascript around 2019 or so. It worked well
enough for the demo, and that was good enough for me.

### forked modules

* <https://github.com/jfhbrook/jp-kernel>
* <https://github.com/jfhbrook/nel>

## korben-twitter

RIP Korben

ca. 2011
2022

He was a good bird

**<./korben-twitter/README.md>**

## nodeboats 2015

At jsconf 2015, there was a competition called "nodeboats" to make and race a remote
control sailboat with some javascript-based IoT gadgets, some motors, a few
takeout containers and some arts-and-crafts. *My* team decided to make a
sailboat, using a lid as the sail.

The actual race was a mess for us, because our design was sensitive to the
rampant connectivity issues we saw when we all tried to use our nodeboats
by the pool at the same time. That said, if memory serves it was otherwise
quite easy to move around once you knew how a sailboat worked!

## prm

`prm` was my first attempt at infrastructure-as-code for COPR. I'm currently
using a script which uses a yaml-based kubernetes-inspired DSL in `coprctl`,
but `prm` used a bespoke bash-based DSL, and was intended to cover more use
cases than just COPR. It was fun to write, but hard to maintain, and in the
end not quite what I wanted.

## PSeudo

A powershell module for faking the UX of the `sudo` command (without the
actual ACL bits), using named pipes. It was based on code I salvaged from
PowerShell Gallery.

It was a cool trick, but you should definitely use [gsudo](https://github.com/gerardog/gsudo)
instead.
