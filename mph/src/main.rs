#[macro_use]
extern crate lazy_static;

extern crate nom;

use anyhow::{anyhow, Error, Result};
use clap::{Parser, Subcommand};

#[cfg(target_os = "macos")]
mod macos;

mod client;
mod daemon;
mod elisp;

use crate::client::Client;
use crate::daemon::Daemon;

#[derive(Debug, Parser)]
#[clap(
    author,
    version,
    about,
    long_about = "a rusty swiss army knife for emacs"
)]
struct Cli {
    #[clap(subcommand)]
    command: Option<Command>,

    file: Option<String>,
}

#[derive(Debug, Subcommand)]
enum Command {
    Start,
    Stop,
    Restart,
    Status,
    Client {
        file: Option<String>,

        #[clap(short, long)]
        version: bool,

        #[clap(short, long)]
        tty: bool,

        #[clap(short, long)]
        create_frame: bool,

        #[clap(long)]
        frame_parameters: Option<String>,

        #[clap(short, long)]
        eval: bool,

        #[clap(short, long)]
        no_wait: bool,

        #[clap(short, long)]
        quiet: bool,

        #[clap(short, long)]
        suppress_output: bool,

        #[clap(long)]
        display: Option<String>,

        #[clap(long)]
        parent_id: Option<String>,

        #[clap(long)]
        socket_name: Option<String>,

        #[clap(long)]
        server_file: Option<String>,

        #[clap(short, long)]
        alternate_editor: Option<String>,

        #[clap(long)]
        tramp: Option<String>,
    },
}

fn main() -> Result<(), Error> {
    let cli = Cli::parse();

    if let Some(command) = cli.command {
        match command {
            Command::Start => {
                let daemon = Daemon::new()?;
                daemon.start()?;
                Ok(())
            }
            Command::Stop => {
                let daemon = Daemon::new()?;
                daemon.stop()?;
                Ok(())
            }
            Command::Restart => {
                let daemon = Daemon::new()?;
                daemon.restart()?;
                Ok(())
            }
            Command::Status => {
                let daemon = Daemon::new()?;
                daemon.status()?;
                Ok(())
            }
            Command::Client {
                file,
                version,
                tty,
                create_frame,
                frame_parameters,
                eval,
                no_wait,
                quiet,
                suppress_output,
                display,
                parent_id,
                socket_name,
                server_file,
                alternate_editor,
                tramp,
            } => {
                let client = Client::new()?;

                let mut cmd = client.command();

                if version {
                    cmd.arg("--version");
                }
                if tty {
                    cmd.arg("--tty");
                }
                if create_frame {
                    cmd.arg("--create-frame");
                }
                if let Some(params) = frame_parameters {
                    cmd.arg("--frame-parameters").arg(params);
                }
                if eval {
                    cmd.arg("--eval");
                }
                if no_wait {
                    cmd.arg("--no-wait");
                }
                if quiet {
                    cmd.arg("--quiet");
                }
                if suppress_output {
                    cmd.arg("--suppress-output");
                }
                if let Some(disp) = display {
                    cmd.arg("--display").arg(disp);
                }
                if let Some(id) = parent_id {
                    cmd.arg("--parent-id").arg(id);
                }
                if let Some(sock) = socket_name {
                    cmd.arg("--socket-name").arg(sock);
                }
                if let Some(f) = server_file {
                    cmd.arg("--server-file").arg(f);
                }
                if let Some(editor) = alternate_editor {
                    cmd.arg("--alternate-editor").arg(editor);
                }
                if let Some(t) = tramp {
                    cmd.arg("--tramp").arg(t);
                }
                if let Some(f) = file {
                    cmd.arg(f);
                }

                let status = cmd.status()?;

                if status.success() {
                    Ok(())
                } else {
                    Err(anyhow!("emacsclient exited with status {:?}", status))
                }
            }
        }
    } else {
        let client = Client::new()?;
        let c = !(client.has_graphical_frame().or_else(|_| {
            let daemon = Daemon::new()?;
            daemon.start()?;
            client.has_graphical_frame()
        })?);

        let mut cmd = client.command();

        cmd.arg("-n");

        if c {
            cmd.arg("-c");
        }

        if let Some(f) = cli.file {
            cmd.arg(f);
        }

        let status = cmd.status()?;

        if status.success() {
            Ok(())
        } else {
            Err(anyhow!("emacsclient exited with status {:?}", status))
        }
    }
}
