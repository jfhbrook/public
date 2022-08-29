use http::Method;

macro_rules! method {
    ($bytes:literal, $method_fn:ident) => {
        pub(crate) fn $method_fn() -> Method {
            Method::from_bytes($bytes).unwrap()
        }
    };
}

method!(b"START", start);
method!(b"STOP", stop);
method!(b"RESTART", restart);
method!(b"RELOAD", reload);
