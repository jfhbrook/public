use anyhow::{Error, Result};
use colored::*;

use korben::{squawk, Budgie};

pub fn main() -> Result<(), Error> {
    let korben = Budgie::new();
    squawk!(korben.burbles());
    Ok(())
}
