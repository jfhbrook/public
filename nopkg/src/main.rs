use anyhow::Result;
use clap::{Parser, Subcommand};

mod cache;
mod commands;
mod lockfile;
mod manifest;
mod solver;

use crate::commands::add::add_command;
use crate::commands::cache::{cache_clean_command, cache_show_command};
use crate::commands::init::init_command;
use crate::commands::install::install_command;
use crate::commands::remove::remove_command;
use crate::commands::show::show_command;
use crate::commands::update::update_command;
use crate::lockfile::{Lockfile, get_lockfile};
use crate::manifest::{Manifest, get_manifest};

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    // Add a new resource
    Add,
    // Work with the artifact cache
    Cache {
        #[command(subcommand)]
        command: CacheCommand,
    },
    // Generate a shell completion script
    Completion,
    // Initialize a new project
    Init,
    // Install configured resources
    Install,
    // Update configured resources
    Update,
    // Show installed resources
    Show,
    // Remove a resource
    Remove,
}

#[derive(Subcommand)]
enum CacheCommand {
    // Add,
    Clean,
    Show,
    // Verify,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Add => add_command(),
        Commands::Cache { command } => match &command {
            CacheCommand::Clean => cache_clean_command(),
            CacheCommand::Show => cache_show_command(),
        },
        Commands::Completion => {
            // TODO: https://docs.rs/clap_complete/latest/clap_complete/
            Ok(())
        }
        Commands::Init => init_command(),
        Commands::Install => install_command(),
        Commands::Update => update_command(),
        Commands::Show => show_command(),
        Commands::Remove => remove_command(),
    }
}
