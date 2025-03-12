use anyhow::Result;
use clap::{Args, CommandFactory, Parser, Subcommand, ValueHint};
use clap_complete::Shell;

mod cache;
mod commands;
mod init;
mod lockfile;
mod manifest;
mod solver;
mod url;

use crate::commands::add::add_command;
use crate::commands::cache::{cache_clean_command, cache_show_command};
use crate::commands::completion::completion_command;
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
    Add {
        url: String,

        #[arg(short, long)]
        file: Option<String>,

        #[arg(short, long, default_value_t = false)]
        unpack: bool,
    },
    // Work with the artifact cache
    Cache {
        #[command(subcommand)]
        command: CacheCommand,
    },
    // Generate a shell completion script
    Completion {
        #[arg(long, value_enum)]
        shell: Option<Shell>,
    },
    // Initialize a new project
    Init {
        #[arg(long)]
        path: Option<String>,

        #[arg(long)]
        overwrite: bool,
    },
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
    // Clear the cache
    #[clap(alias = "nuke")]
    Clear,

    // Show the state of the cache
    Show,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Add { url, file, unpack } => add_command(url, file, unpack),
        Commands::Cache { command } => match &command {
            CacheCommand::Clear => cache_clean_command(),
            CacheCommand::Show => cache_show_command(),
        },
        Commands::Completion { shell } => {
            let mut command = Cli::command();
            return completion_command(*shell, &mut command);
        }
        Commands::Init { path, overwrite } => init_command(path, *overwrite),
        Commands::Install => install_command(),
        Commands::Update => update_command(),
        Commands::Show => show_command(),
        Commands::Remove => remove_command(),
    }
}
