use anyhow::{Error, Result};
use log::{debug, info};
use serde::Serialize;
use tokio::sync::{broadcast, mpsc, oneshot, watch};
use tokio::task;

use crate::config::Config;

#[derive(Debug, Clone, Serialize)]
pub(crate) struct State {}

#[derive(Debug)]
pub(crate) enum StateChange {
    ReceivedExit,
    ReceivedMonitor,
    ReceivedReload { config: Config },
    ReceivedStart { id: usize },
    ReceivedStop { id: usize },
    ReceivedRestart { id: usize },
    ReceivedGetState,
    ReceivedOnLine,
    ReceivedOnStateChange,
    Ready,
    Started { id: usize },
    Stopped { id: usize },
    Exited,
}

#[derive(Debug)]
pub(crate) enum Line {
    StdOut { id: usize, line: String },
    StdErr { id: usize, line: String },
}

type ResponseSender = oneshot::Sender<Response>;

#[derive(Debug)]
pub(crate) enum Command {
    Exit {
        send_response: ResponseSender,
    },
    Monitor {
        send_response: ResponseSender,
    },
    Reload {
        config: Config,
        send_response: ResponseSender,
    },
    Start {
        id: Option<usize>,
        send_response: ResponseSender,
    },
    Stop {
        id: Option<usize>,
        send_response: ResponseSender,
    },
    Restart {
        id: Option<usize>,
        send_response: ResponseSender,
    },
    GetState {
        send_response: ResponseSender,
    },
    OnLine {
        recv_remove: String,
        send_line: oneshot::Sender<Line>,
    },
    OnStateChange {
        recv_remove: String,
        send_change: oneshot::Sender<StateChange>,
    },
}

#[derive(Debug, Clone)]
pub(crate) enum Response {
    Ok,
    State(State),
}

#[derive(Debug, Clone)]
pub(crate) struct Monitor {
    send_command: mpsc::Sender<Command>,
}

impl Monitor {
    pub(crate) async fn new() -> Monitor {
        let (send_command, mut recv_command) = mpsc::channel(32);

        tokio::spawn(async move {
            while let Some(command) = recv_command.recv().await {
                info!("Received command: {:?}", command);
                match command {
                    Command::Exit { send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Exit command");
                        }
                        break;
                    }
                    Command::Monitor { send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Monitor command");
                        }
                    }
                    Command::Reload {
                        config,
                        send_response,
                    } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Reload command");
                        }
                    }
                    Command::Start { id, send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Start({:?}) command", id);
                        }
                    }
                    Command::Stop { id, send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Stop({:?}) command", id);
                        }
                    }
                    Command::Restart { id, send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to Restart({:?}) command", id);
                        }
                    }
                    Command::GetState { send_response } => {
                        let response = Response::Ok;
                        if let Err(_) = send_response.send(response.clone()) {
                            debug!("Failed to send response to GetState command");
                        }
                    }
                    Command::OnLine {
                        recv_remove,
                        send_line,
                    } => {
                        info!("OnLine");
                    }
                    Command::OnStateChange {
                        recv_remove,
                        send_change,
                    } => {
                        info!("OnStateChange");
                    }
                }
            }
        });

        Monitor { send_command }
    }

    pub(crate) async fn request(
        &self,
        command: Command,
        recv_response: oneshot::Receiver<Response>,
    ) -> Result<Response, Error> {
        self.send_command.send(command).await?;

        let response = recv_response.await?;

        Ok(response)
    }
}
