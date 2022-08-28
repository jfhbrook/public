use actix_web::{web, HttpResponse, Resource, Responder};
use serde::{Deserialize, Serialize};

use tokio::sync::oneshot;

mod method;

use crate::data::Config;
use crate::monitor::{Command, Monitor, Response};

#[derive(Debug, Clone)]
pub(crate) struct AppState {
    pub(crate) monitor: Monitor,
}

// TODO: This is all spaghetti and I don't like it.
#[derive(Debug, Clone, Serialize)]
pub(crate) struct UnexpectedResponse {
    message: String,
    expected: String,
    actual: String,
}

impl UnexpectedResponse {
    fn new(expected: &str, actual: Response) -> UnexpectedResponse {
        UnexpectedResponse {
            message: String::from("Unexpected response type"),
            expected: String::from(expected),
            actual: String::from(format!("{:?}", actual)),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub(crate) struct SuccessResponse<T> {
    ok: bool,
    data: T,
}

impl<T> SuccessResponse<T> {
    fn new(data: T) -> SuccessResponse<T> {
        SuccessResponse { ok: true, data }
    }
}

#[derive(Debug, Clone, Serialize)]
struct ErrorResponse {
    ok: bool,
    message: String,
}

impl ErrorResponse {
    fn new(err: anyhow::Error) -> ErrorResponse {
        ErrorResponse {
            ok: false,
            message: String::from(format!("Error: {:?}", err)),
        }
    }
}

pub(crate) fn root_service() -> Resource {
    web::resource("/")
        .route(
            method::reload().to(|state: web::Data<AppState>| async move {
                let (send_response, recv_response) = oneshot::channel();
                match Config::load() {
                    Ok(config) => {
                        match state
                            .monitor
                            .request(
                                Command::Reload {
                                    config,
                                    send_response,
                                },
                                recv_response,
                            )
                            .await
                        {
                            Ok(Response::Ok) => HttpResponse::Ok().json(SuccessResponse::new(())),
                            Ok(res) => HttpResponse::InternalServerError()
                                .json(UnexpectedResponse::new("Response::Ok", res)),
                            Err(err) => {
                                HttpResponse::InternalServerError().json(ErrorResponse::new(err))
                            }
                        }
                    }
                    Err(err) => HttpResponse::InternalServerError().json(ErrorResponse::new(err)),
                }
            }),
        )
        .route(method::exit().to(|state: web::Data<AppState>| async move {
            let (send_response, recv_response) = oneshot::channel();
            match state
                .monitor
                .request(Command::Exit { send_response }, recv_response)
                .await
            {
                Ok(Response::Ok) => HttpResponse::Ok().json(SuccessResponse::new(())),
                Ok(res) => HttpResponse::InternalServerError()
                    .json(UnexpectedResponse::new("Response::Ok", res)),
                Err(err) => HttpResponse::InternalServerError().json(ErrorResponse::new(err)),
            }
        }))
}

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
