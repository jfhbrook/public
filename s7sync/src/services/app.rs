use actix_web::{web, HttpResponse, Resource, Responder};
use serde::{Deserialize, Serialize};

use tokio::sync::oneshot;

use crate::config::Config;
use crate::monitor::{Command, Monitor, Response};
use crate::web::response::{ErrorResponse, SuccessResponse, UnexpectedResponse};
use crate::web::{method, AppState};

pub(crate) fn app_service() -> Resource {
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
