pub(crate) mod config;
pub(crate) mod internal;
pub(crate) mod repositories;
pub(crate) mod server;

use anyhow::{Error, Result};
use clap::{Parser, Subcommand};

use crate::commands::config::{config_command, ConfigCommand};
use crate::commands::internal::{internal_command, InternalCommand};
use crate::commands::repositories::{add_command, remove_command, show_command};
use crate::commands::server::{server_command, ServerCommand};

#[derive(Debug, Parser)]
#[clap(author, version, about, long_about = "Sie7e FileSync")]
pub(crate) struct Cli {
    #[clap(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    // TODO: test
    Config {
        #[clap(subcommand)]
        command: ConfigCommand,
    },
    // TODO: test
    Add {
        #[clap(value_parser)]
        path: Option<String>,

        #[clap(short, long)]
        name: Option<String>,

        #[clap(short, long)]
        remote: Option<String>,
    },
    Remove {
        #[clap(value_parser)]
        selector: Option<String>,
    },
    Show,
    Server {
        #[clap(subcommand)]
        command: ServerCommand,
    },
    App,
    Start {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool,
    },
    Stop {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool,
    },
    Restart {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool,
    },
    Status {
        #[clap(value_parser)]
        selector: Option<String>,

        #[clap(short, long)]
        all: bool,
    },
    Autostart {
        #[clap(subcommand)]
        command: AutostartCommand,
    },
    Daemon {
        #[clap(subcommand)]
        command: DaemonCommand,
    },
    Internal {
        #[clap(subcommand)]
        command: InternalCommand,
    },
    Exit,
}

#[derive(Debug, Subcommand)]
enum AutostartCommand {
    Enable,
    Disable,
}

#[derive(Debug, Subcommand)]
enum DaemonCommand {
    Enable,
    Disable,
    Stop,
    Start,
    Restart,
    Status,
}

pub(crate) fn main_command(cli: Cli) -> Result<(), Error> {
    match cli.command {
        Command::Config { command } => {
            config_command(command)?;
        }
        Command::Add { path, name, remote } => {
            add_command(path, name, remote)?;
        }
        Command::Remove { selector } => {
            remove_command(selector)?;
        }
        Command::Show => {
            show_command()?;
        }
        Command::Server { command } => {
            server_command(command)?;
        }
        Command::App => {
            unimplemented!("app_command");
        }
        Command::Internal { command } => {
            internal_command(command)?;
        }
        default => {
            unimplemented!("{:?}", default);
        }
    };

    Ok(())
}
