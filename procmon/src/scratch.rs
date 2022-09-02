// A rough port of twisted.runner.procmon.
//
// use anyhow::{Error, Result};
use thiserror::Error;

 

struct Process {
    new: Fn() -> std::process::Command
}

struct LineLogger {
    tag: Option<String>
}

impl LineLogger {
    fn line_received(&self, line: String) {
        info!("{tag} {line}", tag=self.tag.unwrap_or(String::from("<none>")), line);
    }
}

// TODO: tokio thread akin to LoggingProtocol

// TODO: what's the analog to reactor.callLater ?
struct Timeout<E: std::Error> {};

impl <E> Timeout<E> {
    fn new() -> Timeout<E> {
        Timeout<E> {}
    }
    fn active(&self) -> Result<bool, E> { Ok(true) }
    fn cancel(&self) -> Result<(), E> { Ok(())}
}

#[derive(Error, Debug)]
pub(crate) enum ProcessMonitorError<N> {
    #[error("Remove {0:?} first")]
    KeyError(N),
}

// I don't want a protocol /per se/ but I *do* need a thing that:
// - holds onto the child
// - handles line output from the process
// - calls the connection_lost callback when the process exits
struct Protocol {
}

struct ProcessMonitor<N> {
    // TODO: these should probably be Durations
    threshold: f64,
    kill_time: f64,
    min_restart_delay: f64,
    max_restart_delay: f64,

    // TODO: logger / log handler
    
    processes: HashMap<N, Process>,
    protocols: HashMap<N, Protocol>,
    delay: HashMap<N, f64>,
    time_started: HashMap<N, f64>,
    murder: HashMap<N, Timeout>,
    restart: HashMap<N, Timeout>,

    running: bool
}

impl ProcessMonitor<N> {
    fn new() -> ProcessMonitor<N> {
        ProcessMonitor {
        }
    }

    fn add_process(&mut self, name: N, new: Fn() -> std::process::Command) -> Result<(), ProcessMonitorError> {
        if self.processes.contains_key(name) {
            return Err(ProcessMonitorError::KeyError(N));
        }

        self.processes.insert(name, Process { new });
        self.delay.insert(name, self.min_restart_delay);
        if self.running {
            self.start_process(name)?;
        }
        Ok()
    }

    fn remove_process(&mut self, name: N) -> Result<(), ProcessMonitorError> {
        self.stop_process(name)?;
        self.processes.remove(name);
        Ok(())
    }

    fn start_service(&mut self) -> Result<(), ProcessMonitorError> {
        self.running = true;
        for (name, process) in self.processes {
            self.start_process(name)?;
        }
        Ok(())
    }

    fn stop_service(&mut self) -> Result<(), ProcessMonitorError> {
        self.running = false;
        for (name, delayed_call) in self.restart {
            delayed_call.cancel()?;
        }

        for name in self.processes.keys() {
            self.stop_process(name)?;
        }

        Ok(())
    }

    // called when a monitored process exits
    fn connection_lost(&mut self, name: N) -> Result<(), ProcessMonitorError> {
        // TODO: all this KeyError stuff - can I push that into a helper? Or use more rusty
        // semantics? perhaps an if let?
        if self.murder.contains_key(name) {
            if self.murder.get(name).ok_or(Err(ProcessMonitorError::KeyError(name)))?.active()? {
                self.murder.get(name).ok_or(Err(ProcessMonitorError::KeyError(name)))?.cancel()?;
            }
            self.murder.remove(name);
        }

        // TODO: self.protocols.remove(name);

        // TODO: this should be in the reactor?
        let next_delay = if self.started_at - self.time_started.get(name).ok_or(Err(ProcessMonitorError::KeyError(name)))? < self.threshold {
            // The process died too fast - backoff
            self.delay.insert(name, std::cmp::min(self.delay.get(name).ok_or(Err(ProcessMonitorError::KeyError(name)))? * 2, self.max_restart_delay));
            self.delay.get(name).ok_or(Err(ProcessMonitorError::KeyError(name)))?
        } else {
            self.delay.insert(name, self.min_restart_delay);
            0
        };

        if self.running && self.processes.contains_key(name) {
            self.restart.insert(name, Timeout::new(/* self.start_process */))
        }

        Ok(())
    }

    fn start_process(&mut self, name: N) -> Result<(), ProcessMonitorError> {
        // TODO: If a protocol instance already exists, it means the process is
        // already running
        // if self.protocols.contains_key(name) { return Ok(()); }
        let process = self.processes.get(name).ok_or(ProcessMonitorError::KeyError(name))?;

        // let proto = LoggingProtocol::new(name, self);
        // self.protocols.insert(name, proto);
        // TODO: time.now? or someting actually from the generic Reactor?
        self.time_started.insert(name, /* reactor.seconds() */);

        // TODO: twisted uses a protocol to let the process write out in the
        // background. Instead, we want to send log lines etc., to a channel.
        // Tokio also might have a different abstraction? what is the Command
        // abstraction capable of?
        let process = process.new().spawn()?;

        // TODO: what to do with process lol
        Ok(())
    }

    fn force_stop_process(&self, process: std::process::Child) {
        // It's presumed any Error is becaues the process exited already. It's
        // plausible there could be other reasons but they seem unlikely and
        // the process API doesn't support any Kinds in its API contract.
        process.kill().ok_or(Ok(())).unwrap()
    }

    fn stop_process(&mut self, name: N) -> Result<(), ProcessMonitorError> {
        if !self.processes.contains_key(name) {
            return Err(ProcessMonitorError::KeyError(name));
        }

        // TODO: lol
        if let Some(proto) = self.protocols.get(name) {
            let child = proto.child;
            // TODO: a whole thing in rust
            // https://stackoverflow.com/questions/49210815/how-do-i-send-a-signal-to-a-child-subprocess
            send_sigterm(child).ok_or(Ok(())?;
        } else {
            // TODO: lmao
            self.murder.insert(name, Timeout::new(self.kill_time, &self.force_stop_process, child));
        }
    }

    fn restart_all(&mut self) -> Result<(), ProcessMonitorError> {
        for name in self.processes.keys() {
            self.stop_process(name)?;
        }
    }
}
