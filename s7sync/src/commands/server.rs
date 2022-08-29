use crate::logger::init_logger;
use crate::monitor::Monitor;
use crate::web::server;
use anyhow::{Error, Result};
use clap::Subcommand;

use crate::web::client::Client;

#[derive(Debug, Subcommand)]
pub(crate) enum ServerCommand {
    Start,
    Stop,
}

pub(crate) fn server_command(command: ServerCommand) -> Result<(), Error> {
    match command {
        ServerCommand::Start => start_command(),
        ServerCommand::Stop => stop_command(),
    }
}

#[tokio::main]
pub(crate) async fn start_command() -> Result<(), Error> {
    init_logger()?;

    let monitor = Monitor::new().await;

    server::start(&monitor).await?;
    Ok(())
}

pub(crate) fn stop_command() -> Result<(), Error> {
    init_logger()?;

    let client = Client::new();

    println!("{:?}", client.stop_server()?);

    Ok(())
}
