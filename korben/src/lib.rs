use std::include_bytes;
use std::str;

use markov::Chain;

pub struct Budgie {
    chain: Chain<String>,
}

impl Budgie {
    pub fn new() -> Budgie {
        let pet_sounds = str::from_utf8(include_bytes!("pet_sounds.txt")).unwrap();
        let mut chain = Chain::new();

        for sound in pet_sounds.split("\n") {
            chain.feed_str(&sound);
        }

        Budgie { chain }
    }

    pub fn burbles(&self) -> String {
        let burbles = self.chain.generate_str();
        if burbles.len() > 0 {
            burbles
        } else {
            String::from("*beak grindies*")
        }
    }
}

#[macro_export]
macro_rules! squawk {
    ($burbles:expr) => {
        println!("{}", $burbles.cyan());
    };
}
