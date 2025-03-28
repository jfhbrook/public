use anyhow::Result;
use clap::{CommandFactory, Parser, Subcommand}; // ValueHint
use clap_complete::Shell;
use tracing::{error, info};

mod cache;
mod commands;
mod lockfile;
mod log;
mod manifest;
mod solver;

use crate::commands::add::add_command;
use crate::commands::cache::{
    cache_add_command, cache_destroy_command, cache_remove_command, cache_show_command,
};
use crate::commands::completion::completion_command;
use crate::commands::init::init_command;
use crate::commands::install::install_command;
use crate::commands::remove::remove_command;
use crate::commands::show::show_command;
use crate::commands::update::update_command;
use crate::log::{LogFormat, LogLevel, configure_logging};

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Cli {
    #[arg(short, long, value_enum, default_value_t = LogLevel::Warn)]
    log_level: LogLevel,

    #[arg(short, long, value_enum, default_value_t = LogFormat::Cli)]
    format: LogFormat,

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

        #[arg(short, long, default_value = "./nopkg.toml")]
        manifest_path: String,
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
        #[arg(short, long, default_value = "./nopkg.toml")]
        path: String,

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
    /// Add a url to the cache
    Add {
        url: String,
    },

    /// Remove a url from the cache
    Remove {
        url: String,
    },

    // Clear the cache
    #[clap(alias = "nuke")]
    Destroy,

    // Show the state of the cache
    Show,
}

fn log_result(cli: &Cli, result: Result<()>) -> Result<()> {
    if let Err(err) = result {
        return match &cli.format {
            LogFormat::Json => {
                error!("{}", err);
                Ok(())
            }
            _ => Err(err),
        };
    };

    match &cli.command {
        Commands::Completion { shell: _ } => {}
        _ => {
            info!("ok");
        }
    };

    Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Completion { shell: _ } => {}
        _ => {
            configure_logging(&cli.log_level, &cli.format);
            info!("it worked if it ends with ok");
        }
    };

    let result = match &cli.command {
        Commands::Add {
            url,
            file,
            unpack,
            manifest_path,
        } => add_command(url, file, unpack, manifest_path),
        Commands::Cache { command } => match &command {
            CacheCommand::Add { url } => cache_add_command(url).await,
            CacheCommand::Remove { url } => cache_remove_command(url),
            CacheCommand::Destroy => cache_destroy_command(),
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
    };

    log_result(&cli, result)?;
    Ok(())
}
