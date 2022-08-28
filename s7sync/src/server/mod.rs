use actix_web::{web, HttpResponse, Resource, Responder};
use serde::Deserialize;

mod method;

use crate::monitor::Monitor;

#[derive(Debug, Clone)]
pub(crate) struct AppState {
    pub(crate) monitor: Monitor,
}

pub(crate) fn root_service() -> Resource {
    web::resource("/").route(method::reload().to(|| async { HttpResponse::Ok().body("reload") }))
}

pub(crate) fn config_service() -> Resource {
    web::resource("/config")
        .route(method::get().to(|| async { HttpResponse::Ok().body("show config") }))
}

#[derive(Debug, Deserialize)]
struct Setting {
    name: String,
}

pub(crate) fn setting_service() -> Resource {
    web::resource("/config/{name}")
        .route(method::get().to(|setting: web::Path<Setting>| async move {
            HttpResponse::Ok().body(format!("get: {:?}", setting))
        }))
        .route(method::put().to(
            |setting: web::Path<Setting>, value: web::Json<String>| async move {
                HttpResponse::Ok().body(format!("set: {:?} = {:?}", setting, value))
            },
        ))
}

pub(crate) fn monitor_service() -> Resource {
    web::resource("/monitor").route(
        method::get()
            .to(|state: web::Data<AppState>| async { HttpResponse::Ok().body("monitor status") }),
    )
}

#[derive(Debug, Deserialize)]
struct Process {
    index: usize,
}

pub(crate) fn process_service() -> Resource {
    web::resource("/monitor/{index}")
        .route(method::get().to(
            |state: web::Data<AppState>, process: web::Path<Process>| async move {
                HttpResponse::Ok().body(format!("status: {:?}", process))
            },
        ))
        .route(method::start().to(
            |state: web::Data<AppState>, process: web::Path<Process>| async move {
                HttpResponse::Ok().body(format!("start: {:?}", process))
            },
        ))
        .route(method::stop().to(
            |state: web::Data<AppState>, process: web::Path<Process>| async move {
                HttpResponse::Ok().body(format!("stop: {:?}", process))
            },
        ))
        .route(method::restart().to(
            |state: web::Data<AppState>, process: web::Path<Process>| async move {
                HttpResponse::Ok().body(format!("restart: {:?}", process))
            },
        ))
}
