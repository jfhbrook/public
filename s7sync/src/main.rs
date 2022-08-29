use anyhow::{Error, Result};
use clap::Parser;

mod commands;
mod config;
mod logger;
mod monitor;
mod platform;
mod services;
mod web;

use crate::commands::{main_command, Cli};

fn main() -> Result<(), Error> {
    let cli = Cli::parse();

    main_command(cli)
}
