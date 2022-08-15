use anyhow::{Error, Result};
use camino::Utf8PathBuf;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Debug)]
pub(crate) struct RepositoryConfig {
    path: String,
    remote: String
}

#[derive(Deserialize, Serialize, Debug)]
pub(crate) struct Config {
    min_poll_wait: Option<u64>,
    min_commit_wait: Option<u64>,
    min_pull_wait: Option<u64>,
    max_pull_wait: Option<u64>,
    min_push_wait: Option<u64>,
    idle_timeout: Option<u64>,
    session_timeout: Option<u64>,
    commit_message: Option<String>,
    repositories: Option<Vec<RepositoryConfig>>
}

pub(crate) fn load_config(path: Utf8PathBuf) -> Result<Config, Error> {
    unimplemented!("load_config");
}

pub(crate) fn save_config(config: Config, path: Utf8PathBuf) -> Result<(), Error> {
    unimplemented!("save_config");
}
