use rand::Rng;
use std::include_bytes;
use std::str;

extern crate clap;

use clap::{App, Arg};

use egg_mode::error::Error;
use egg_mode::tweet::{DraftTweet, Tweet};
use egg_mode::{KeyPair, Response, Token};

#[macro_use]
extern crate log;

use markov::Chain;
use simplelog::{ColorChoice, Config, LevelFilter, TermLogger, TerminalMode};

const CONSUMER_KEY: &str = env!("TWITTER_CONSUMER_KEY");
const CONSUMER_SECRET: &str = env!("TWITTER_CONSUMER_SECRET");
const ACCESS_TOKEN: &str = env!("TWITTER_ACCESS_TOKEN");
const ACCESS_SECRET: &str = env!("TWITTER_ACCESS_SECRET");

struct Budgie {
    chain: Chain<String>,
    laziness: f32,
    token: egg_mode::Token,
}

impl Budgie {
    fn new(laziness: f32) -> Budgie {
        let token = Token::Access {
            consumer: KeyPair::new(CONSUMER_KEY, CONSUMER_SECRET),
            access: KeyPair::new(ACCESS_TOKEN, ACCESS_SECRET),
        };

        let pet_sounds = str::from_utf8(include_bytes!("pet_sounds.txt")).unwrap();
        let mut chain = Chain::new();

        for sound in pet_sounds.split("\n") {
            chain.feed_str(&sound);
        }

        Budgie {
            chain: chain,
            laziness: laziness,
            token: token,
        }
    }

    fn feels_like_tweeting(&self) -> bool {
        let mut rng = rand::thread_rng();
        let gumption = rng.gen_range(0.0..1.0);

        gumption > self.laziness
    }

    fn squawk(&self) -> String {
        self.chain.generate_str()
    }

    async fn tweet(&self, text: String) -> Result<Response<Tweet>, Error> {
        let tweet = DraftTweet::new(text);

        tweet.send(&self.token).await
    }
}

#[tokio::main]
pub async fn main() -> Result<(), Error> {
    TermLogger::init(
        LevelFilter::Info,
        Config::default(),
        TerminalMode::Mixed,
        ColorChoice::Auto,
    )
    .unwrap();

    let argv = App::new("Korben the Tweetin' Budgie")
        .version("5.0")
        .author("Josh H")
        .arg(
            Arg::with_name("laziness")
                .short("l")
                .long("laziness")
                .value_name("laziness")
                .help("A float between 0 and 1 - the higher, the less likely Korben is to tweet"),
        )
        .get_matches();

    let laziness: f32 = argv
        .value_of("laziness")
        .unwrap_or("0.0")
        .parse()
        .unwrap_or(0.0);

    let korben = Budgie::new(laziness);

    info!("The birdseed understander as logged on 😤");

    if korben.feels_like_tweeting() {
        let squawkings = korben.squawk();

        info!("Tweeting some stupid shit like '{}'...", squawkings);

        match korben.tweet(squawkings).await {
            Ok(response) => {
                info!(
                    "READ MY TWEET LAUL https://twitter.com/korbenisabird/status/{}",
                    response.id
                );

                info!("Done!");

                Ok(())
            }
            Err(err) => {
                error!("Some total BS happened: {}", err);
                Err(err)
            }
        }
    } else {
        info!("I don't feel like tweeting and you can't make me!");
        Ok(())
    }
}
