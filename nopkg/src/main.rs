use anyhow::Result;
use clap::{Parser, Subcommand};

mod lockfile;
mod manifest;
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
    List,
    // Verify,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Add => Ok(()),
        Commands::Cache { command } => match &command {
            CacheCommand::Clean => Ok(()),
            CacheCommand::List => Ok(()),
        },
        Commands::Completion => {
            // TODO: https://docs.rs/clap_complete/latest/clap_complete/
            Ok(())
        }
        Commands::Init => Ok(()),
        Commands::Install => Ok(()),
        Commands::Update => Ok(()),
        Commands::Show => Ok(()),
        Commands::Remove => Ok(()),
    }
}
