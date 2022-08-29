use actix_web::{web, Resource};

use thiserror::Error;

use crate::config::{Config, ConfigError};
use crate::monitor::{Command, MonitorError, Response};
use crate::web::response::{responder, WebError};
use crate::web::{reload, stop, AppState};

#[derive(Error, Debug)]
pub(crate) enum AppError {
    #[error("{0:?}")]
    ConfigError(#[from] ConfigError),

    #[error("{0:?}")]
    MonitorError(#[from] MonitorError),
}

impl Into<WebError> for AppError {
    fn into(self: Self) -> WebError {
        WebError::FlagrantError(format!("{:?}", self))
    }
}

pub(crate) fn app_service() -> Resource {
    web::resource("/")
        .route(reload().to(|state: web::Data<AppState>| async move {
            responder::<Response, AppError, _>(|| async {
                let config = Config::load()?;
                let res = state.monitor.request(Command::Reload { config }).await?;
                Ok(res)
            })
            .await
        }))
        .route(stop().to(|state: web::Data<AppState>| async move {
            responder::<Response, AppError, _>(|| async {
                let res = state.monitor.request(Command::Exit).await?;
                Ok(res)
            })
            .await
        }))
}
