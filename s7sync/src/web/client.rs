use crate::web::method;
use anyhow::{Error, Result};

use crate::monitor::Response;
use crate::web::response::ResponseBody;

pub(crate) struct Client {}

impl Client {
    // TODO: plumb config + get connstring that way
    pub(crate) fn new() -> Client {
        Client {}
    }

    pub(crate) fn stop_server(&self) -> Result<Response, Error> {
        let res = reqwest::blocking::Client::builder()
            .build()?
            .request(method::stop(), "https://127.0.0.1:8080")
            .send()?
            .json::<ResponseBody<Response>>()?;

        let res = match res {
            ResponseBody::Ok(res) => Ok(res),
            ResponseBody::Err(err) => Err(err),
        }?;

        Ok(res)
    }
}
