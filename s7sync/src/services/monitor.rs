use actix_web::{web, HttpResponse, Resource};
use serde::Deserialize;

use crate::monitor::{Command, MonitorError, Response};
use crate::web::{method, AppState};

use crate::web::response::responder;

pub(crate) fn monitor_service() -> Resource {
    web::resource("/monitor").route(method::get().to(|state: web::Data<AppState>| async move {
        responder::<Response, MonitorError, _>(|| async {
            let state = state.clone();
            let state = state.monitor.request(Command::GetState).await?;
            Ok(state)
        })
        .await
    }))
}

#[derive(Debug, Deserialize)]
struct ProcessPath {
    index: usize,
}

pub(crate) fn process_service() -> Resource {
    web::resource("/monitor/{index}")
        .route(method::get().to(
            |state: web::Data<AppState>, process: web::Path<ProcessPath>| async move {
                HttpResponse::Ok().body(format!("status: {:?}", process))
            },
        ))
        .route(method::start().to(
            |state: web::Data<AppState>, process: web::Path<ProcessPath>| async move {
                HttpResponse::Ok().body(format!("start: {:?}", process))
            },
        ))
        .route(method::stop().to(
            |state: web::Data<AppState>, process: web::Path<ProcessPath>| async move {
                HttpResponse::Ok().body(format!("stop: {:?}", process))
            },
        ))
        .route(method::restart().to(
            |state: web::Data<AppState>, process: web::Path<ProcessPath>| async move {
                HttpResponse::Ok().body(format!("restart: {:?}", process))
            },
        ))
}
