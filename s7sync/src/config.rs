use anyhow::{anyhow, Error, Result};
use directories::ProjectDirs;
use serde::{Deserialize, Serialize};
use std::fs::{self, create_dir_all, File, OpenOptions};
use std::io::{ErrorKind::NotFound, Write};
use std::path::{Path, PathBuf};

#[derive(Deserialize, Serialize, Debug)]
pub(crate) struct Repository {
    path: String,
    remote: String,
}

#[derive(Deserialize, Serialize, Debug)]
pub(crate) struct Config {
    min_poll_wait: u64,
    min_commit_wait: u64,
    min_pull_wait: u64,
    max_pull_wait: u64,
    min_push_wait: u64,
    idle_timeout: u64,
    session_timeout: u64,
    commit_message: String,
    repositories: Vec<Repository>,
}

impl std::default::Default for Config {
    fn default() -> Self {
        Self {
            min_poll_wait: 1,
            min_commit_wait: 15,
            min_pull_wait: 600,
            max_pull_wait: 7200,
            min_push_wait: 600,
            idle_timeout: 600,
            session_timeout: 1800,
            commit_message: "Automatic commit by Sie7e FileSync".to_string(),
            repositories: Vec::<Repository>::new(),
        }
    }
}

// This code is heavily inspired by confy but uses json instead of toml and
// hard-codes everything to my use case:
//
//     https://docs.rs/confy/0.4.0/src/confy/lib.rs.html
//
// It's available under MIT, X11 or Apache 2.0 licenses.

fn file_path(dir: &Path) -> Result<PathBuf, Error> {
    Ok([
        dir.to_str().ok_or(anyhow!("path apparently not unicode?"))?,
        "s7sync.json",
    ]
    .iter()
    .collect())
}

impl Config {
    pub(crate) fn load() -> Result<Config, Error> {
        let project =
            ProjectDirs::from("com", "sie7elabs", "s7sync").ok_or(anyhow!("no project?"))?;
        let dir = project.config_dir();
        let path = file_path(&dir)?;

        match fs::read_to_string(path) {
            Ok(json) => Ok(serde_json::from_str(&json)?),
            // TODO: I might want to do something more sophisticated here, like
            // catch this error in the command layer and execute an init flow
            Err(ref e) if e.kind() == NotFound => {
                create_dir_all(&dir)?;
                let cfg = Config::default();
                cfg.save()?;
                Ok(cfg)
            }
            Err(e) => Err(anyhow!(e)),
        }
    }

    pub(crate) fn save(&self) -> Result<(), Error> {
        let project =
            ProjectDirs::from("com", "sie7elabs", "s7sync").ok_or(anyhow!("no project?"))?;
        let dir = project.config_dir();
        let path = file_path(&dir)?;

        let mut f = OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(&path)?;

        f.write_all(serde_json::to_string(self)?.as_bytes())?;
        Ok(())
    }
}
