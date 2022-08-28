use anyhow::{Error, Result};
use log::{debug, info};
use tokio::sync::{broadcast, mpsc, oneshot, watch};
use tokio::task;

use crate::config::Config;

#[derive(Debug)]
pub(crate) struct Status {}

#[derive(Debug)]
pub(crate) enum StatusChange {
    ReceivedExit,
    ReceivedMonitor,
    ReceivedReload { config: Config },
    ReceivedStart { id: usize },
    ReceivedStop { id: usize },
    ReceivedRestart { id: usize },
    ReceivedGetStatus,
    ReceivedOnLine,
    ReceivedOnStatusChange,
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

type Responder<T> = oneshot::Sender<Result<T, Error>>;

pub(crate) enum Command {
    Exit {
        send_response: Option<Responder<()>>,
    },
    Monitor {
        send_response: Option<Responder<()>>,
    },
    Reload {
        config: Config,
        send_response: Option<Responder<()>>,
    },
    Start {
        id: Option<usize>,
        send_response: Option<Responder<()>>,
    },
    Stop {
        id: Option<usize>,
        send_response: Option<Responder<()>>,
    },
    Restart {
        id: Option<usize>,
        send_response: Option<Responder<()>>,
    },
    GetStatus {
        send_response: Responder<()>,
    },
    OnLine {
        recv_remove: String,
        send_line: oneshot::Sender<Line>,
    },
    OnStatusChange {
        recv_remove: String,
        send_change: oneshot::Sender<StatusChange>,
    },
}

async fn monitor() -> mpsc::Sender<Command> {
    let (send_command, mut recv_command) = mpsc::channel(32);

    tokio::spawn(async move {
        while let Some(command) = recv_command.recv().await {
            match command {
                Command::Exit { send_response } => {
                    info!("Received Exit");
                }
                Command::Monitor { send_response } => {
                    info!("Received Monitor");
                }
                Command::Reload {
                    config,
                    send_response,
                } => {
                    info!("Received Reload");
                }
                Command::Start { id, send_response } => {
                    info!("Received Start({:?})", id);
                }
                Command::Stop { id, send_response } => {
                    info!("Received Stop({:?})", id);
                }
                Command::Restart { id, send_response } => {
                    info!("Received Restart({:?})", id);
                }
                Command::GetStatus { send_response } => {
                    info!("Received GetStatus");
                }
                Command::OnLine {
                    recv_remove,
                    send_line,
                } => {
                    info!("Received OnLine");
                }
                Command::OnStatusChange {
                    recv_remove,
                    send_change,
                } => {
                    info!("OnStatusChange");
                }
            }
        }
    });

    send_command
}

