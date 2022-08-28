use actix_web::{rt, web, App, HttpServer};
use anyhow::{Error, Result};

use crate::logger::init_logger;
use crate::monitor::{Command, Monitor};
use crate::server::{
    config_service, monitor_service, process_service, root_service, setting_service, AppState,
};

#[tokio::main]
pub(crate) async fn server_command() -> Result<(), Error> {
    init_logger()?;

    let monitor = Monitor::new().await;

    HttpServer::new(move || {
        let state = AppState {
            monitor: monitor.clone(),
        };
        App::new()
            .app_data(state.clone())
            .service(root_service())
            .service(config_service())
            .service(setting_service())
            .service(monitor_service())
            .service(process_service())
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await?;

    Ok(())
}
