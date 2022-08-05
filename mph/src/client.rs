use std::process::Command;

#[cfg(target_os = "windows")]
use std::fs::metadata;

use anyhow::{anyhow, Error, Result};
use which::which;

#[cfg(target_os = "macos")]
use crate::macos::MacOSApp;

#[derive(Debug)]
pub(crate) struct Client {
    path: String,
}

#[cfg(target_os = "windows")]
const EMACSCLIENT: &str = "C:\\Program Files\\Emacs\\x86_64\\bin\\emacsclient.exe";

const HAS_GRAPHICAL_FRAME: &str = include_str!("../elisp/has_graphical_frame.el");

impl Client {
    #[cfg(target_os = "linux")]
    pub fn new() -> Result<Client, Error> {
        let wh = which("emacsclient")?;
        let path = wh
            .into_os_string()
            .into_string()
            .or_else(|err| Err(anyhow!("error stringifying path: {:?}", err)))?;
        Ok(Client { path })
    }

    #[cfg(target_os = "macos")]
    pub fn new() -> Result<Client, Error> {
        let app = MacOSApp::new()?;
        // TODO: the Right Way to do this is to get really angry at PathBuf for
        // a day
        let mut raw_path: String = app.path.to_owned();
        raw_path.push_str("/Contents/MacOS/bin/emacsclient");
        Ok(Client { path: raw_path })
    }

    // TODO: We need to search Program Files et al for emacs
    #[cfg(target_os = "windows")]
    pub fn new() -> Result<Client, Error> {
        match metadata(EMACSCLIENT) {
            Ok(md) => {
                if md.is_file() {
                    return Ok(Client {
                        path: String::from(EMACSCLIENT),
                    });
                }
            }
            _ => {
                // TODO: log at debug
            }
        };
        let wh = which("emacsclient")?;
        let path = wh
            .into_os_string()
            .into_string()
            .or_else(|err| Err(anyhow!("error stringifying path: {:?}", err)))?;
        Ok(Client { path })
    }

    pub fn command(&self) -> Command {
        Command::new(&self.path)
    }

    pub fn eval(&self, expr: &str) -> Result<String, Error> {
        let output = Command::new(&self.path).arg("-e").arg(expr).output()?;

        if !output.status.success() {
            return Err(anyhow!(
                "emacsclient exited with status {:?}",
                output.status
            ));
        }

        let utf8 = String::from_utf8_lossy(&output.stdout).into_owned();

        let trimmed = utf8.as_str().trim();

        Ok(String::from(trimmed))
    }

    pub fn has_graphical_frame(&self) -> Result<bool, Error> {
        let result = self.eval(HAS_GRAPHICAL_FRAME)?;
        Ok(result == "t")
    }
}
