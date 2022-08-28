pub(crate) mod method;
pub(crate) mod server;
pub(crate) mod response;

use crate::monitor::{Monitor, Response};

#[derive(Debug, Clone)]
pub(crate) struct AppState {
    pub(crate) monitor: Monitor,
}
