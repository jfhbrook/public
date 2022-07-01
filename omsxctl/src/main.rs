use std::env;
use std::io::{BufWriter, Write};
use std::net::Shutdown;
use std::os::unix::net::UnixStream;
use std::path::PathBuf;

use anyhow::{anyhow, Error, Result};
use clap::Parser;
use colored::*;
use glob::glob;
use rustyline::error::ReadlineError;
use rustyline::Editor;
use tracing::{event, span, Level};
use tracing_subscriber;
use xml::reader::{EventReader, XmlEvent};

struct Client<'a> {
    reader: EventReader<&'a UnixStream>,
    writer: BufWriter<&'a UnixStream>,
}

enum Response {
    Ok(String),
    Nok(String),
}

// TODO: add support for json and/or xml output in addition to pretty printing
fn print_response(response: &Response) {
    match response {
        Response::Ok(data) => {
            println!("{}: {}", "ok".green(), data);
        }
        Response::Nok(data) => {
            println!("{}: {}", "nok".red(), data);
        }
    };
}

impl<'a> Client<'a> {
    fn new(socket: &'a UnixStream) -> Result<Client<'a>, Error> {
        let span = span!(Level::DEBUG, "Client::new");
        let _enter = span.enter();

        let writer = BufWriter::new(socket);
        let mut reader = EventReader::new(socket);

        loop {
            match reader.next() {
                Ok(XmlEvent::StartElement { name, .. }) if name.local_name == "openmsx-output" => {
                    event!(Level::DEBUG, "openmsx is ready.");
                    return Ok(Client { reader, writer });
                }
                Ok(event) => {
                    event!(Level::TRACE, "xml event: {event:?}", event = event);
                }
                Err(err) => {
                    return Err(anyhow!(err));
                }
            };
        }
    }

    fn request(&mut self, command: &String) -> Result<Response, Error> {
        let span = span!(Level::DEBUG, "sending a command");
        let _enter = span.enter();

        self.writer.write(b"<command>")?;
        self.writer.write(command.as_bytes())?;
        self.writer.write(b"</command>\n")?;
        self.writer.flush()?;

        event!(Level::DEBUG, "sent command: {command}", command = command);

        let mut ok: String = String::from("nok");

        loop {
            match self.reader.next() {
                Ok(XmlEvent::StartElement {
                    name, attributes, ..
                }) if name.local_name == "reply" => {
                    ok = attributes
                        .iter()
                        .find(|attr| attr.name.local_name == "result")
                        .map(|attr| attr.value.to_owned())
                        .ok_or_else(|| anyhow!("result attribute is undefined"))?;
                    break;
                }
                Ok(event) => {
                    event!(Level::TRACE, "xml event: {event:?}", event = event);
                }
                Err(err) => {
                    return Err(anyhow!(err));
                }
            };
        }

        let mut data = String::new();

        loop {
            match self.reader.next() {
                Ok(XmlEvent::Characters(chunk)) => {
                    data.push_str(chunk.as_str());
                }
                Ok(XmlEvent::EndElement { name, .. }) if name.local_name == "reply" => {
                    event!(Level::DEBUG, "reply: {ok:?}. {data}", ok = ok, data = data);

                    return if ok == "ok" {
                        Ok(Response::Ok(data))
                    } else {
                        Ok(Response::Nok(data))
                    };
                }
                Ok(event) => {
                    event!(Level::TRACE, "xml event: {event:?}", event = event);
                }
                Err(err) => {
                    return Err(anyhow!(err));
                }
            }
        }
    }
}

fn find_socket() -> Result<PathBuf, Error> {
    let span = span!(Level::DEBUG, "looking for a socket");
    let _enter = span.enter();

    let user = env::var("USER")?;

    let selector: String = format!("/tmp/openmsx-{}/socket.*", user);

    let mut path: Option<PathBuf> = None;

    for entry in glob(selector.as_str())? {
        if let Ok(p) = entry {
            path = Some(p);
            break;
        }
    }
    if let Some(sock) = path {
        Ok(sock)
    } else {
        Err(anyhow!("socket could not be found."))
    }
}

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    eval: Option<String>,

    #[clap(short, long)]
    address: Option<String>,
}

fn main() -> Result<(), Error> {
    tracing_subscriber::fmt::init();

    let span = span!(Level::DEBUG, "main");
    let _enter = span.enter();

    let user = env::var("USER")?;
    let history_file = format!("/home/{}/.omsxctl_history", user);

    let args = Args::parse();
    let socket = if let Some(addr) = &args.address {
        UnixStream::connect(addr)?
    } else {
        UnixStream::connect(find_socket()?)?
    };

    let mut server = Client::new(&socket)?;

    if let Some(command) = &args.eval {
        let response = server.request(&command)?;
        print_response(&response);
    } else {
        let mut rl = Editor::<()>::new();

        if rl.load_history(history_file.as_str()).is_err() {
            event!(Level::DEBUG, ".omsxctl_history not found.");
        }

        println!();
        println!("for available commands, visit: https://openmsx.org/manual/commands.html");
        println!();

        loop {
            let readline = rl.readline("openmsx> ");
            match readline {
                Ok(line) => {
                    rl.add_history_entry(line.as_str());
                    let response = server.request(&line)?;
                    print_response(&response);
                }
                Err(ReadlineError::Interrupted) => {
                    event!(Level::DEBUG, "user sent ctrl-c");
                    break;
                }
                Err(ReadlineError::Eof) => {
                    event!(Level::DEBUG, "user sent ctrl-d");
                    break;
                }
                other => {
                    // TODO: attempt to save history before propagating errors
                    other?;
                }
            }
        }
        rl.save_history(history_file.as_str())?;
    }

    // TODO: shut down the write side first, then read output until the xml
    // output gets properly capped
    socket.shutdown(Shutdown::Both)?;

    Ok(())
}
