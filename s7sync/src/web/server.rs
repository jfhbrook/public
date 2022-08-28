use actix_web::{rt, web, App, HttpServer};
use anyhow::{Error, Result};

use crate::logger::init_logger;
use crate::monitor::{Command, Monitor};
use crate::server::{config_service, monitor_service, process_service, setting_service, AppState};

use crate::services::app::app_service;

pub(crate) async fn start(monitor: &Monitor) -> Result<(), Error> {
    let monitor = monitor.clone();
    HttpServer::new(move || {
        let state = AppState {
            monitor: monitor.clone(),
        };
        App::new()
            .app_data(state.clone())
            .service(app_service())
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
