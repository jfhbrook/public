#[cfg(target_os = "windows")]
use std::fs::metadata;

use anyhow::{anyhow, Error, Result};
use std::{thread, time};

lazy_static! {
    static ref RETRY_WAIT: time::Duration = time::Duration::from_millis(200);
    static ref RETRY_MAX_WAIT: time::Duration = time::Duration::from_millis(15000);
}

#[cfg(target_os = "windows")]
use which::which;

#[cfg(target_os = "windows")]
const RUNEMACS: &str = "C:\\Program Files\\Emacs\\x86_64\\bin\\runemacs.exe";

// TODO: This needs to check the status code and error on a 1
#[cfg(target_os = "linux")]
fn systemctl(cmd: &str) -> Result<(), Error> {
    let status = std::process::Command::new("systemctl")
        .arg(cmd)
        .arg("--user")
        .arg("emacs")
        .status()?;

    if status.success() {
        Ok(())
    } else {
        Err(anyhow!("systemctl exited with status {:?}", status))
    }
}

#[cfg(target_os = "windows")]
pub fn find_emacs() -> Result<String, Error> {
    // TODO: Push this copypasta into a windows.rs file
    match metadata(RUNEMACS) {
        Ok(md) => {
            if md.is_file() {
                return Ok(String::from(RUNEMACS));
            }
        }
        _ => {
            // TODO: log at debug
        }
    };
    let wh = which("runemacs.exe")?;
    let path = wh
        .into_os_string()
        .into_string()
        .or_else(|err| Err(anyhow!("error stringifying path: {:?}", err)))?;
    Ok(path)
}

use crate::client::Client;

#[derive(Debug)]
pub(crate) struct Daemon {
    client: Client,
}

impl Daemon {
    pub fn new() -> Result<Daemon, Error> {
        let client = Client::new()?;

        Ok(Daemon { client })
    }

    pub fn ok(&self) -> bool {
        match self.client.eval("'ok") {
            Ok(_) => true,
            Err(_) => false,
        }
    }

    pub fn wait_until_ok(&self) -> Result<(), Error> {
        let now = time::Instant::now();
        let mut ok = self.ok();
        while !ok {
            if now.elapsed() > *RETRY_MAX_WAIT {
                return Err(anyhow!("Took too long for Emacs to start!"));
            }

            thread::sleep(*RETRY_WAIT);

            ok = self.ok();
        }

        Ok(())
    }

    pub fn wait_while_ok(&self) -> Result<(), Error> {
        let now = time::Instant::now();
        let mut ok = self.ok();
        while ok {
            if now.elapsed() > *RETRY_MAX_WAIT {
                return Err(anyhow!("Took too long for Emacs to start!"));
            }

            thread::sleep(*RETRY_WAIT);

            ok = self.ok();
        }

        Ok(())
    }

    #[cfg(target_os = "linux")]
    pub fn start(&self) -> Result<(), Error> {
        systemctl("start")?;
        Ok(())
    }

    #[cfg(target_os = "linux")]
    pub fn stop(&self) -> Result<(), Error> {
        systemctl("stop")?;
        Ok(())
    }

    #[cfg(target_os = "linux")]
    pub fn restart(&self) -> Result<(), Error> {
        systemctl("restart")?;
        Ok(())
    }

    #[cfg(target_os = "linux")]
    pub fn status(&self) -> Result<(), Error> {
        systemctl("status")?;
        Ok(())
    }

    #[cfg(target_os = "macos")]
    pub fn start(&self) -> Result<(), Error> {
        let status = std::process::Command::new("open")
            .arg("-a")
            .arg("Emacs")
            .status()?;

        if !status.success() {
            return Err(anyhow!("open exited with status {:?}", status));
        }

        self.wait_until_ok()?;

        Ok(())
    }

    #[cfg(target_os = "macos")]
    pub fn stop(&self) -> Result<(), Error> {
        // TODO: is this the most graceful way to do this?
        self.client.eval("(save-buffers-kill-terminal)")?;

        self.wait_while_ok()?;

        Ok(())
    }

    #[cfg(target_os = "macos")]
    pub fn restart(&self) -> Result<(), Error> {
        self.stop()?;
        self.start()
    }

    #[cfg(target_os = "macos")]
    pub fn status(&self) -> Result<(), Error> {
        let status = std::process::Command::new("osascript")
            .arg("-e")
            .arg("tell application \"System Events\" to set emacs to (get name of processes where background only is false and name contains \"Emacs\")
if count of emacs > 0 then
  set output to (\"✅] \" & (item 1 of emacs) & \".app\n\")
  repeat with e in (rest of emacs)
    set output to (output & \"❓ \" & e & \".app\n\")
  end repeat
else
  set output to (\"❌ \" & \"Emacs.app\" & \"\n\")
end if
copy output to stdout")
            .status()?;

        if !status.success() {
            return Err(anyhow!("open exited with status {:?}", status));
        }

        Ok(())
    }

    #[cfg(target_os = "windows")]
    pub fn start(&self) -> Result<(), Error> {
        let emacs = find_emacs()?;
        let status = std::process::Command::new("powershell.exe")
            .arg("-Command")
            .arg(format!("Start-Process '{}'", emacs))
            .status()?;

        if status.success() {
            Ok(())
        } else {
            Err(anyhow!("powershell.exe exited with status {:?}", status))
        }
    }

    #[cfg(target_os = "windows")]
    pub fn stop(&self) -> Result<(), Error> {
        // TODO: is this the most graceful way to do this?
        // TODO: seems a lil copypasta
        self.client.eval("(save-buffers-kill-terminal)")?;

        self.wait_while_ok()?;

        Ok(())
    }

    #[cfg(target_os = "windows")]
    pub fn restart(&self) -> Result<(), Error> {
        self.stop()?;
        self.start()
    }

    #[cfg(target_os = "windows")]
    pub fn status(&self) -> Result<(), Error> {
        let status = std::process::Command::new("powershell.exe")
            .arg("-Command")
            .arg("Get-Process -ProcessName emacs")
            .status()?;

        if status.success() {
            Ok(())
        } else {
            Err(anyhow!("powershell.exe exited with status {:?}", status))
        }
    }
}
