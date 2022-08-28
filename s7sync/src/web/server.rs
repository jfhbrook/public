use actix_web::{App, HttpServer};

use crate::monitor::Monitor;
use crate::web::AppState;

use crate::services::app::app_service;
use crate::services::monitor::{monitor_service, process_service};

pub(crate) async fn start(monitor: &Monitor) -> Result<(), std::io::Error> {
    let monitor = monitor.clone();
    HttpServer::new(move || {
        let state = AppState {
            monitor: monitor.clone(),
        };
        App::new()
            .app_data(state.clone())
            .service(app_service())
            .service(monitor_service())
            .service(process_service())
    })
    // returns an IOError
    .bind(("127.0.0.1", 8080))?
    .run()
    .await?;

    Ok(())
}
