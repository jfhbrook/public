use actix_web::{rt, web, App, HttpServer};
use anyhow::{Error, Result};

use crate::logger::init_logger;
use crate::monitor::{Command, Monitor};
use crate::server::{
    config_service, monitor_service, process_service, root_service, setting_service, AppState,
};
use crate::web::server;

#[tokio::main]
pub(crate) async fn server_command() -> Result<(), Error> {
    init_logger()?;

    let monitor = Monitor::new().await;

    server::start(&monitor).await
}
