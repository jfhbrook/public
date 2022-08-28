use actix_web::{web, HttpResponse, Resource, Responder};
use serde::{Deserialize, Serialize};

use tokio::sync::oneshot;

use crate::config::Config;
use crate::monitor::{Command, Monitor, Response};
use crate::web::{method, AppState};

use crate::server::{ErrorResponse, SuccessResponse, UnexpectedResponse};

pub(crate) fn config_service() -> Resource {
    web::resource("/config").route(method::get().to(|| async {
        match Config::load() {
            Ok(config) => HttpResponse::Ok().json(SuccessResponse::new(config)),
            Err(err) => HttpResponse::InternalServerError().json(ErrorResponse::new(err)),
        }
    }))
}

#[derive(Debug, Deserialize)]
struct Setting {
    name: String,
}

pub(crate) fn setting_service() -> Resource {
    web::resource("/config/{name}")
        .route(method::get().to(|setting: web::Path<Setting>| async move {
            match Config::load() {
                Ok(config) => HttpResponse::Ok().body("TODO"),
                Err(err) => HttpResponse::InternalServerError().json(ErrorResponse::new(err)),
            }
        }))
        .route(method::put().to(
            |setting: web::Path<Setting>, value: web::Json<String>| async move {
                HttpResponse::Ok().body(format!("set: {:?} = {:?}", setting, value))
            },
        ))
}
