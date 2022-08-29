use anyhow::{anyhow, Error, Result};
use clap::Subcommand;
use log::{debug, info};
use tabled::{Table, Tabled};

use crate::config::Config;
use crate::logger::init_logger;

#[derive(Debug, Subcommand)]
pub(crate) enum ConfigCommand {
    Show,
    Get {
        #[clap(value_parser)]
        name: String,
    },
    Set {
        #[clap(value_parser)]
        name: String,

        #[clap(value_parser)]
        value: String,
    },
}

pub(crate) fn config_command(command: ConfigCommand) -> Result<(), Error> {
    match command {
        ConfigCommand::Show => show_command(),
        ConfigCommand::Get { name } => get_command(name),
        ConfigCommand::Set { name, value } => set_command(name, value),
    }
}

#[derive(Tabled)]
struct SettingRow<'t> {
    name: &'t str,
    value: &'t str,
}

// TODO: It /should/ be possible to DRY this up with some procedural macros.
// They may even exist already! But for now, a little boilerplate.

fn show_command() -> Result<(), Error> {
    let config = Config::load()?;

    // TODO: impl custom Debug trait for a Settings repository
    let min_poll_wait = config.min_poll_wait.to_string();
    let min_commit_wait = config.min_commit_wait.to_string();
    let min_pull_wait = config.min_pull_wait.to_string();
    let max_pull_wait = config.max_pull_wait.to_string();
    let min_push_wait = config.min_push_wait.to_string();
    let idle_timeout = config.idle_timeout.to_string();
    let session_timeout = config.session_timeout.to_string();
    let commit_message = config.commit_message;

    let settings = vec![
        SettingRow {
            name: "min_poll_wait",
            value: min_poll_wait.as_str(),
        },
        SettingRow {
            name: "min_commit_wait",
            value: min_commit_wait.as_str(),
        },
        SettingRow {
            name: "min_pull_wait",
            value: min_pull_wait.as_str(),
        },
        SettingRow {
            name: "max_pull_wait",
            value: max_pull_wait.as_str(),
        },
        SettingRow {
            name: "min_push_wait",
            value: min_push_wait.as_str(),
        },
        SettingRow {
            name: "idle_timeout",
            value: idle_timeout.as_str(),
        },
        SettingRow {
            name: "session_timeout",
            value: session_timeout.as_str(),
        },
        SettingRow {
            name: "commit_message",
            value: commit_message.as_str(),
        },
    ];

    println!("{}", Table::new(settings).to_string());

    Ok(())
}

// TODO: support "raw" and "json"
fn get_command(name: String) -> Result<(), Error> {
    // TODO: configure simplelog to go to stderr so I can log with abandon
    let config = Config::load()?;

    println!("{}", config.get_setting(name)?);

    Ok(())
}

fn set_command(name: String, value: String) -> Result<(), Error> {
    init_logger()?;

    let mut config = Config::load()?;

    debug!("Current configuration:\n\n{config:#?}", config = config);

    info!("Setting {name:?} = {value:?}", name = name, value = value);

    config.set_setting(name, value)?;

    debug!("Updated configuration:\n\n{config:#?}", config = config);

    Ok(())
}
