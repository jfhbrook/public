# korben-twitter

This is the twitter bot which powers [@korbenisabird](https://twitter.com/korbenisabird). It is written in rust.

## building

Before building, you need to create a `.env` file in this folder with the
following variables:

- `TWITTER_CONSUMER_KEY` - Your twitter consumer key
- `TWITTER_CONSUMER_SECRET` - Your twitter consumer secret
- `TWITTER_ACCESS_TOKEN` - Your twitter access token
- `TWITTER_ACCESS_SECRET` - Your twitter access secret

You can generate these values by creating an app at [twitter's developer console](https://developer.twitter.com/en/apps).

**NOTE**: The compiled binary will have your twitter creds embedded in it and
anybody with a copy will be able to tweet with your account! Treat it as
a secret!

### tasks

This project uses [just](https://github.com/casey/just) to run tasks. For the
most part these are thin wrappers around cargo with `.env` file loading.

Available recipes:

- `just check` - type-check everything
- `just run` - run the bot locally
- `just build` - use cargo to compile a release build
- `just build-raspi` - use cross to compile a release build for raspberry pi

### raspberry pi + cross-compilation

I deploy this on a raspberry pi in my basement, so I need to cross-compile.
To do this, you'll need to install [cross](https://github.com/rust-embedded/cross).

## usage

```
Korben the Tweetin' Budgie 5.0
Josh H

USAGE:
    korben-twitter [OPTIONS]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

OPTIONS:
    -l, --laziness <laziness>    A float between 0 and 1 - the higher, the less likely Korben is to tweet
```

The `--laziness` flag sets a likelihood that the bot will tweet. For example,
if laziness is set to 0.8, the command will abstain from tweeting 80% of the
time.

## deployment

I deploy korben-twitter as a cron job. I do this with ansible, but what gets
written to the crontab looks something like this:

```
0 0 * * * bash -c 'sleep $((RANDOM \\% 3600))' && korben-twitter --laziness 0.2' >> /var/log/korben-twitter.log 2>&1 && echo 'INFO: @korbenisabird exited successfully!' >> /var/log/korben-twitter.log || echo 'FATAL: @korbenisabird exited with a failure status!' >> /var/log/korben-twitter.log
```

This command runs korben-twitter every hour, with a random delay of up to an
hour, with logging to /var/log/korben-twitter.log.

## tweet frequency analysis

The `tweet_frequency_analysis.ipynb` contains an analysis I ran to estimate
how often @korbenisabird would tweet under different architectures. An old
version of korben-twitter (this is probably the fourth rewrite) would wait a
random period of time between tweets, unlike this version which runs in a cron
job. When changing strategies, I wanted to understand how the frequency of
tweets would change, and how I should tune things to get the best frequency.

### license

korben-twitter is licensed Apache 2.0.
