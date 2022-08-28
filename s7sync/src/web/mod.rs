pub(crate) mod method;
pub(crate) mod response;
pub(crate) mod server;

use crate::monitor::Monitor;

#[derive(Debug, Clone)]
pub(crate) struct AppState {
    pub(crate) monitor: Monitor,
}
