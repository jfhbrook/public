use anyhow::{anyhow, Error, Result};
use clap::{Parser, Subcommand};
use log::{debug, info, warn, error};

mod commands;
mod config;
mod logger;
mod platform;

use crate::config::{load_config, save_config};
use crate::logger::init_logger;
use crate::commands::internal::{InternalCommand, internal_command};

#[derive(Debug, Parser)]
#[clap(
    author,
    version,
    about,
    long_about = "Sie7e FileSync"
)]
struct Cli {
    #[clap(subcommand)]
    command: Option<Command>
}

#[derive(Debug, Subcommand)]
enum Command {
    Add {
        #[clap(value_parser)]
        repository: String
    },
    Remove {
        #[clap(value_parser)]
        repository: String
    },
    Ui,
    Start {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool
    },
    Stop {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool
    },
    Restart {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool
    },
    Status {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool
    },
    Autostart {
        #[clap(subcommand)]
        command: AutostartCommand
    },
    Daemon {
        #[clap(subcommand)]
        command: DaemonCommand
    },
    Internal {
        #[clap(subcommand)]
        command: InternalCommand
    }
}

#[derive(Debug, Subcommand)]
enum AutostartCommand {
    Enable,
    Disable
}

#[derive(Debug, Subcommand)]
enum DaemonCommand {
    Enable,
    Disable,
    Stop,
    Start,
    Restart,
    Status
}

fn main() -> Result<(), Error> {
    let cli = Cli::parse();

    match cli.command {
        None => {
            init_logger()?;
            info!("default behavior!");
        },
        Some(Command::Ui) => {
            unimplemented!("TODO: launch the UI!");
        },
        Some(Command::Internal { command }) => {
            internal_command(command);
        },
        default => {
            unimplemented!("{:?}", default);
        }
    };

    Ok(())
}
