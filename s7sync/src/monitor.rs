use anyhow::{Error, Result};
use log::{debug, info, warn};
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
    Exit,
    Monitor,
    Reload { config: Config },
    Start { id: Option<usize> },
    Stop { id: Option<usize> },
    Restart { id: Option<usize> },
    GetState,
    /*
    OnLine {
        recv_remove: String,
        send_line: oneshot::Sender<Line>,
    },
    OnStateChange {
        recv_remove: String,
        send_change: oneshot::Sender<StateChange>,
    },
    */
}

#[derive(Debug, Clone)]
pub(crate) enum Response {
    Ok,
    State(State),
}

#[derive(Debug, Clone)]
pub(crate) struct Monitor {
    send_command: mpsc::Sender<(Command, Option<oneshot::Sender<Response>>)>,
}

impl Monitor {
    pub(crate) async fn new() -> Monitor {
        let (send_command, mut recv_command): (
            mpsc::Sender<(Command, Option<oneshot::Sender<Response>>)>,
            mpsc::Receiver<(Command, Option<oneshot::Sender<Response>>)>,
        ) = mpsc::channel(32);

        tokio::spawn(async move {
            while let Some((command, send_response)) = recv_command.recv().await {
                let respond = |response: Response| {
                    if let Some(tx) = send_response {
                        if let Err(err) = tx.send(response) {
                            warn!("Error while sending response: {:?}", err);
                        }
                    } else {
                        debug!("Response: {:?}", response);
                    }
                };
                info!("Received command: {:?}", command);
                match command {
                    Command::Exit => {
                        let response = Response::Ok;
                        respond(response.clone());
                        break;
                    }
                    Command::Monitor => {
                        let response = Response::Ok;
                        respond(response.clone())
                    }
                    Command::Reload { config } => {
                        let response = Response::Ok;
                        respond(response.clone());
                    }
                    Command::Start { id } => {
                        let response = Response::Ok;
                        respond(response.clone());
                    }
                    Command::Stop { id } => {
                        let response = Response::Ok;
                        respond(response.clone());
                    }
                    Command::Restart { id } => {
                        let response = Response::Ok;
                        respond(response.clone());
                    }
                    Command::GetState => {
                        let response = Response::Ok;
                        respond(response.clone());
                    } /*
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
                      */
                }
            }
        });

        Monitor { send_command }
    }

    pub(crate) async fn request(&self, command: Command) -> Result<Response, Error> {
        let (tx, rx) = oneshot::channel();
        self.send_command.send((command, Some(tx))).await?;

        let response = rx.await?;

        Ok(response)
    }
}
