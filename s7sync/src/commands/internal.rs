use anyhow::{Error, Result};
use clap::{ArgEnum, Subcommand};
use log::{debug, error, info, warn};

use crate::logger::init_logger;
use crate::platform::get_platform;

#[derive(Debug, Subcommand)]
pub(crate) enum InternalCommand {
    Log {
        #[clap(arg_enum, short, long)]
        level: Option<LogLevel>,

        #[clap(short, long)]
        pid: Option<String>,

        #[clap(value_parser, multiple_values = true)]
        message: Vec<String>,
    },
    Platform,
}

pub(crate) fn internal_command(command: InternalCommand) -> Result<(), Error> {
    match command {
        InternalCommand::Log {
            level,
            pid,
            message,
        } => {
            log_command(level, pid, message)?;
        }
        InternalCommand::Platform => {
            println!("{:?}", get_platform());
        }
    };

    Ok(())
}

#[derive(PartialEq, Debug, Clone, ArgEnum)]
pub(crate) enum LogLevel {
    Debug,
    Info,
    Warn,
    Error,
    Output,
}

pub(crate) fn log_command(
    level: Option<LogLevel>,
    pid: Option<String>,
    message: Vec<String>,
) -> Result<(), Error> {
    init_logger()?;

    let msg = message.join(" ");

    match level {
        Some(LogLevel::Debug) => {
            if let Some(p) = pid {
                debug!("({pid}) {message}", pid = p, message = msg);
            } else {
                debug!("{message}", message = msg);
            }
        }
        Some(LogLevel::Info) | None => {
            if let Some(p) = pid {
                info!("({pid}) {message}", pid = p, message = msg);
            } else {
                info!("{message}", message = msg);
            }
        }
        Some(LogLevel::Warn) => {
            if let Some(p) = pid {
                warn!("({pid}) {message}", pid = p, message = msg);
            } else {
                warn!("{message}", message = msg);
            }
        }
        Some(LogLevel::Error) => {
            if let Some(p) = pid {
                error!("({pid}) {message}", pid = p, message = msg);
            } else {
                error!("{message}", message = msg);
            }
        }
        Some(LogLevel::Output) => {
            if let Some(p) = pid {
                println!("({pid}) {message}", pid = p, message = msg);
            } else {
                println!("{message}", message = msg);
            }
        }
    };

    Ok(())
}
