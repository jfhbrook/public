pub(crate) mod client;
pub(crate) mod method;
pub(crate) mod response;
pub(crate) mod server;

use actix_web::Route;

pub use actix_web::web::{delete, get, head, patch, post, put, trace};

use crate::monitor::Monitor;

macro_rules! method {
    ($method_fn:ident) => {
        pub(crate) fn $method_fn() -> Route {
            Route::new().method(crate::web::method::$method_fn())
        }
    };
}

method!(start);
method!(stop);
method!(restart);
method!(reload);

#[derive(Debug, Clone)]
pub(crate) struct AppState {
    pub(crate) monitor: Monitor,
}
