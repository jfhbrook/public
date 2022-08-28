use actix_web::{rt, web, App, HttpServer};
use anyhow::{Error, Result};

use crate::logger::init_logger;
use crate::monitor::{Command, Monitor};
use crate::web::server;

#[tokio::main]
pub(crate) async fn server_command() -> Result<(), Error> {
    init_logger()?;

    let monitor = Monitor::new().await;

    server::start(&monitor).await
}
