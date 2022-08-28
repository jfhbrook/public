use actix_web::{web, HttpResponse, Resource, Responder};
use serde::{Deserialize, Serialize};

use tokio::sync::oneshot;

use crate::data::Config;
use crate::monitor::{Command, Monitor, Response};
use crate::web::{method, AppState};

use crate::server::{ErrorResponse, SuccessResponse, UnexpectedResponse};

pub(crate) fn monitor_service() -> Resource {
    web::resource("/monitor").route(method::get().to(|state: web::Data<AppState>| async move {
        let (send_response, recv_response) = oneshot::channel();
        match state
            .monitor
            .request(Command::GetState { send_response }, recv_response)
            .await
        {
            Ok(Response::State(data)) => HttpResponse::Ok().json(data),
            // TODO: Internal error type
            Ok(res) => HttpResponse::InternalServerError()
                .json(UnexpectedResponse::new("Response::State", res)),
            Err(err) => HttpResponse::InternalServerError().json(ErrorResponse::new(err)),
        }
    }))
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
