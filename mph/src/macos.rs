use anyhow::{anyhow, Error, Result};
use serde::Deserialize;

#[cfg(target_os = "macos")]
#[derive(Debug, Deserialize)]
pub(crate) struct MacOSApp {
    _name: String,
    arch_kind: String,
    info: Option<String>,
    lastModified: String,
    obtained_from: Option<String>,
    pub(crate) path: String,
    signed_by: Option<Vec<String>>,
    version: Option<String>,
}

#[cfg(target_os = "macos")]
#[derive(Debug, Deserialize)]
struct SystemProfilerData {
    SPApplicationsDataType: Vec<MacOSApp>,
}

#[cfg(target_os = "macos")]
impl MacOSApp {
    pub fn new() -> Result<MacOSApp, Error> {
        let output = std::process::Command::new("system_profiler")
            .arg("-json")
            .arg("SPApplicationsDataType")
            .output()?;

        let from_utf8 = String::from_utf8_lossy(&output.stdout);

        let profiler_data: SystemProfilerData =
            serde_json::from_str(from_utf8.into_owned().as_str())?;

        profiler_data
            .SPApplicationsDataType
            .into_iter()
            .find(|app| app._name == "Emacs")
            .ok_or(anyhow!("could not find emacs app - are you on MacOS?"))
    }
}
