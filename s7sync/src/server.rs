use serde::Serialize;

use crate::monitor::Response;

// NOTE: This module is the remnants of an earlier structure for this project
// and contains response-mapping code. Everything else lives in the web
// submodule.
//
// TODO: Create implicit mappings (the Into trait?) between struts/enums returned
// by the controllers and these responses

#[derive(Debug, Clone, Serialize)]
pub(crate) struct UnexpectedResponse {
    message: String,
    expected: String,
    actual: String,
}

impl UnexpectedResponse {
    pub(crate) fn new(expected: &str, actual: Response) -> UnexpectedResponse {
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
    pub(crate) fn new(data: T) -> SuccessResponse<T> {
        SuccessResponse { ok: true, data }
    }
}

#[derive(Debug, Clone, Serialize)]
pub(crate) struct ErrorResponse {
    ok: bool,
    message: String,
}

impl ErrorResponse {
    pub(crate) fn new(err: anyhow::Error) -> ErrorResponse {
        ErrorResponse {
            ok: false,
            message: String::from(format!("Error: {:?}", err)),
        }
    }
}
