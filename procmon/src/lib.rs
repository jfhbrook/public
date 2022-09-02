use std::collections::HashMap;
use std::time::{Duration, Instant};
use thiserror::Error;
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Child;
use tokio::sync::broadcast;
use tokio::sync::mpsc;

#[derive(Debug, Error)]
pub enum SpawnError {
    #[error("{0:?}")]
    IoError(#[from] std::io::Error),

    #[error("{0:?}")]
    MpscSendError(#[from] mpsc::error::SendError<Event>),

    #[error("{0:?}")]
    BroadcastSendError(#[from] broadcast::error::SendError<Event>),

    #[error("{0:?}")]
    BroadcastRecvError(#[from] broadcast::error::RecvError),
}

#[derive(Debug, Clone)]
pub enum Signal {
    Term,
    Kill,
    Stdin(String),
}

#[derive(Debug, Clone)]
pub enum Event {
    StdoutLine(String),
    StderrLine(String),
    Exit(Option<i32>),
}

// TODO: make this a dyn trait
pub struct Process<'p> {
    _spawn: &'p dyn Fn() -> Result<Child, std::io::Error>,
}

impl<'p> Process<'p> {
    pub fn new(factory: &'p dyn Fn() -> Result<Child, std::io::Error>) -> Process {
        Process { _spawn: factory }
    }

    pub fn spawn(&self) -> Result<Child, std::io::Error> {
        (self._spawn)()
    }
}

pub fn spawn(
    process: &Process,
) -> Result<(mpsc::Sender<Signal>, broadcast::Receiver<Event>), SpawnError> {
    let (tx_signal, mut rx_signal) = mpsc::channel(32);
    let (tx_event, rx_event) = broadcast::channel(32);

    let mut child = process.spawn()?;
    let stdin = child.stdin.take();
    let stdout = child.stdout.take();
    let stderr = child.stderr.take();
    if let Some(stdout) = stdout {
        let tx = tx_event.clone();
        let mut reader = BufReader::new(stdout).lines();

        tokio::spawn(async move {
            while let Some(line) = reader.next_line().await? {
                tx.send(Event::StdoutLine(line))?;
            }

            // TODO: use a semaphore to trigger the Exit event
            // tx.send(Event::StdoutClose)?;

            Ok::<(), SpawnError>(())
        });
    }

    if let Some(stderr) = stderr {
        let tx = tx_event.clone();
        let mut reader = BufReader::new(stderr).lines();

        tokio::spawn(async move {
            while let Some(line) = reader.next_line().await? {
                tx.send(Event::StderrLine(line))?;
            }

            // TODO: use a semaphore to trigger the Exit event
            // tx.send(Event::StderrClose)?;

            Ok::<(), SpawnError>(())
        });
    }

    tokio::spawn(async move {
        loop {
            tokio::select! {
                status = child.wait() => {
                    let status = status?;
                    tx_event.clone().send(Event::Exit(status.code()))?;
                    break;
                }
                Some(signal) = rx_signal.recv() => {
                    match signal {
                        Signal::Term => {
                            unimplemented!("TODO: send a term signal");
                        },
                        Signal::Kill => {
                            child.kill().await?;
                        },
                        Signal::Stdin(line) => {
                            unimplemented!("send a line over stdin");
                        }
                    }
                }
            }
        }

        Ok::<(), SpawnError>(())
    });

    Ok((tx_signal, rx_event))
}

#[cfg(test)]
mod test_spawn {
    use super::{spawn, Event, Process, SpawnError};
    use std::process::Stdio;
    use tokio::process::Command;

    #[tokio::test]
    async fn test_stdout_stderr() -> Result<(), SpawnError> {
        let process = Process::new(&|| {
            Command::new("bash")
                .arg("-c")
                .arg("echo 'writing to stdout'; echo 'writing to stderr' 1>&2")
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
        });

        let (_, mut rx) = spawn(&process)?;

        let mut stdout: Vec<String> = vec![];
        let mut stderr: Vec<String> = vec![];
        let mut exit: Option<i32> = None;

        while let Ok(event) = rx.recv().await {
            match event {
                Event::StdoutLine(line) => {
                    stdout.push(line.clone());
                }
                Event::StderrLine(line) => {
                    stderr.push(line.clone());
                }
                Event::Exit(code) => exit = code,
            }
        }

        assert_eq!(exit, Some(0));
        assert_eq!(stdout, vec!["writing to stdout"]);
        assert_eq!(stderr, vec!["writing to stderr"]);
        Ok(())
    }
}

struct ProcmonOptions {
    threshold: Duration,
    kill_time: Duration,
    min_restart_delay: Duration,
    max_restart_delay: Duration,
}

struct ProcessMonitor<N> {
    processes: HashMap<N, Process>,
    delay: HashMap<N, Duration>,
    time_started: HashMap<N, Instant>,
    // murder: HashMap<N, Timeout>,
    // restart: HashMap<N, Timeout>,

    // running: bool
}
