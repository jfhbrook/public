use actix_web::HttpResponse;
use serde::{Deserialize, Serialize};
use std::future::Future;
use thiserror::Error;

#[derive(Error, Debug, Clone, Deserialize, Serialize)]
pub(crate) enum WebError {
    #[error("Flagrant Error: {0}")]
    FlagrantError(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub(crate) enum ResponseBody<T> {
    Ok(T),
    Err(WebError),
}

pub(crate) async fn responder<T, E, F>(handler: impl Fn() -> F) -> HttpResponse
where
    T: Serialize,
    E: Into<WebError>,
    F: Future<Output = Result<T, E>>,
{
    match handler().await {
        Ok(response) => HttpResponse::Ok().json(ResponseBody::Ok(response)),
        Err(err) => HttpResponse::InternalServerError().json(err.into()),
    }
}
