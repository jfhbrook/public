use actix_web::Route;
use http::Method;

pub use actix_web::web::{delete, get, head, patch, post, put, trace};

macro_rules! method {
    ($bytes:literal, $method_fn:ident) => {
        pub(crate) fn $method_fn() -> Route {
            Route::new().method(Method::from_bytes($bytes).unwrap())
        }
    };
}

method!(b"START", start);
method!(b"STOP", stop);
method!(b"RESTART", restart);
method!(b"RELOAD", reload);
