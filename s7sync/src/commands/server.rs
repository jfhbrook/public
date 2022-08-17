use actix_web::{rt, App, HttpServer};
use anyhow::{Error, Result};

use crate::logger::init_logger;
use crate::server::{
    config_service, monitor_service, process_service, root_service, setting_service,
};

pub(crate) fn server_command() -> Result<(), Error> {
    init_logger()?;

    rt::System::new().block_on(
        HttpServer::new(|| {
            App::new()
                .service(root_service())
                .service(config_service())
                .service(setting_service())
                .service(monitor_service())
                .service(process_service())
        })
        .bind(("127.0.0.1", 8080))?
        .run(),
    )?;

    Ok(())
}
