use directories::ProjectDirs;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::env;
use std::fs::{self, create_dir_all, metadata, OpenOptions};
use std::io::{ErrorKind::NotFound, Write};
use std::path::{Path, PathBuf};
use std::process::Command;

use thiserror::Error;

#[derive(Error, Debug)]
pub(crate) enum ConfigError {
    #[error("Could not find home directory")]
    HomeDirectoryError,

    #[error("Could not build path to s7sync.json")]
    ConfigPathError,

    #[error("{0:?}")]
    IOError(#[from] std::io::Error),

    #[error("{0:?}")]
    Utf8Error(#[from] std::str::Utf8Error),

    #[error("{0:?}")]
    JsonError(#[from] serde_json::Error),

    #[error("{0:?} is not a git repository and no remote was specified")]
    UnknownRemoteError(PathBuf),

    #[error("Could not extract repository name from directory")]
    RepositoryNameError(String),

    #[error("Error converting OsString to String")]
    OsStringError(std::ffi::OsString),

    #[error("Repository {0} already registered at {1}")]
    UniqueRepositoryError(String, String),

    #[error("Repository {0} not found")]
    RepositoryNotFoundError(usize),

    #[error("No repositories found for selector {0}")]
    RepositorySearchError(String),

    #[error("Setting {0} not found")]
    SettingNotFound(String),

    #[error("Failed to parse value {0:?}")]
    ParseIntError(#[from] std::num::ParseIntError),
}

// config directory and file stuff

fn project_dirs() -> Result<ProjectDirs, ConfigError> {
    ProjectDirs::from("com", "sie7elabs", "s7sync").ok_or(ConfigError::HomeDirectoryError)
}

fn file_path(dir: &Path) -> Result<PathBuf, ConfigError> {
    // TODO: can I get rid of some of this conversion nonsense by using camino?
    Ok([
        dir.to_str().ok_or(ConfigError::ConfigPathError)?,
        "s7sync.json",
    ]
    .iter()
    .collect())
}

// git-related stuff
// TODO: move these into a git submodule

// Checks if a path is a git repository
// TODO: generic path-like and camino
fn is_git_repository(path: &PathBuf) -> Result<bool, ConfigError> {
    let mut path = path.clone();

    path.push(".git");

    let md = metadata(path)?;

    Ok(md.is_dir())
}

// a cheeky shell call to get the remote
// TODO: generic path-like and camino
fn git_remote(path: &PathBuf) -> Result<Option<String>, ConfigError> {
    // TODO: In windows, search in well-known locations if not in path
    let output = Command::new("git")
        .args(["config", "--get", "remote.origin.url"])
        .current_dir(&path)
        .output()?;
    let stdout = std::str::from_utf8(&output.stdout)?;
    let stdout = stdout.trim().to_string();

    if stdout.len() > 0 {
        Ok(Some(stdout))
    } else {
        Ok(None)
    }
}

// The "config" is really more of a database, storing global settings and
// a list of repositories to watch.
#[derive(Deserialize, Serialize, Debug)]
pub(crate) struct Config {
    pub(crate) min_poll_wait: u64,
    pub(crate) min_commit_wait: u64,
    pub(crate) min_pull_wait: u64,
    pub(crate) max_pull_wait: u64,
    pub(crate) min_push_wait: u64,
    pub(crate) idle_timeout: u64,
    pub(crate) session_timeout: u64,
    pub(crate) commit_message: String,
    pub(crate) repositories: Vec<Repository>,
}

// These are the default settings!
impl std::default::Default for Config {
    fn default() -> Self {
        Self {
            min_poll_wait: 1,
            min_commit_wait: 15,
            min_pull_wait: 10 * 60,
            max_pull_wait: 15 * 60,
            min_push_wait: 10 * 60,
            idle_timeout: 10 * 60,
            session_timeout: 30 * 60,
            commit_message: "Automatic commit by Sie7e FileSync".to_string(),
            repositories: Vec::<Repository>::new(),
        }
    }
}

// Load and save the file. This is heavily inspired by confy: https://docs.rs/confy/0.4.0/src/confy/lib.rs.html

impl Config {
    pub(crate) fn load() -> Result<Config, ConfigError> {
        let project = project_dirs()?;
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
            Err(e) => Err(ConfigError::IOError(e)),
        }
    }

    pub(crate) fn save(&self) -> Result<(), ConfigError> {
        let project = project_dirs()?;
        let dir = project.config_dir();
        let path = file_path(&dir)?;

        let mut f = OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(&path)?;

        f.write_all(serde_json::to_string_pretty(self)?.as_bytes())?;
        Ok(())
    }

    pub(crate) fn get_setting(&self, name: String) -> Result<String, ConfigError> {
        if name == "min_poll_wait" {
            Ok(format!("{}", self.min_poll_wait))
        } else if name == "min_commit_wait" {
            Ok(format!("{}", self.min_commit_wait))
        } else if name == "min_pull_wait" {
            Ok(format!("{}", self.min_pull_wait))
        } else if name == "max_pull_wait" {
            Ok(format!("{}", self.max_pull_wait))
        } else if name == "min_push_wait" {
            Ok(format!("{}", self.min_push_wait))
        } else if name == "idle_timeout" {
            Ok(format!("{}", self.idle_timeout))
        } else if name == "session_timeout" {
            Ok(format!("{}", self.session_timeout))
        } else if name == "commit_message" {
            Ok(format!("{}", self.commit_message))
        } else {
            Err(ConfigError::SettingNotFound(name))
        }
    }

    pub(crate) fn set_setting(&mut self, name: String, value: String) -> Result<(), ConfigError> {
        if name == "min_poll_wait" {
            self.min_poll_wait = value.parse()?;
        } else if name == "min_commit_wait" {
            self.min_commit_wait = value.parse()?;
        } else if name == "min_pull_wait" {
            self.min_pull_wait = value.parse()?;
        } else if name == "max_pull_wait" {
            self.max_pull_wait = value.parse()?;
        } else if name == "min_push_wait" {
            self.min_push_wait = value.parse()?;
        } else if name == "idle_timeout" {
            self.idle_timeout = value.parse()?;
        } else if name == "session_timeout" {
            self.session_timeout = value.parse()?;
        } else if name == "commit_message" {
            self.commit_message = value;
        } else {
            return Err(ConfigError::SettingNotFound(name));
        };

        Ok(())
    }
}

// A repository model
#[derive(Deserialize, Serialize, Debug, Clone)]
pub(crate) struct Repository {
    pub(crate) name: String,
    pub(crate) path: String,
    pub(crate) remote: Option<String>,
}

// The git-repository evans-repository!
pub(crate) struct Repositories<'c> {
    config: &'c mut Config,
}

impl<'c> Repositories<'c> {
    pub(crate) fn new(config: &mut Config) -> Repositories {
        Repositories { config }
    }

    fn unique_name(&self, default: &String) -> Result<String, ConfigError> {
        let mut names: HashSet<&String> = HashSet::new();

        for repo in &self.config.repositories {
            names.insert(&repo.name);
        }

        let mut i = 1;

        loop {
            let name = if i == 1 {
                default.clone()
            } else {
                format!("{} ({})", default, i)
            };
            if !names.contains(&name) {
                return Ok(name);
            }
            i += 1;
        }
    }

    pub(crate) fn create(
        &self,
        repository: &Option<String>,
        name: &Option<String>,
        remote: &Option<String>,
    ) -> Result<Repository, ConfigError> {
        let mut path = if let Some(repo) = repository {
            PathBuf::from(repo)
        } else {
            env::current_dir()?
        };

        // If we don't have a remote then we won't be able to clone it if it's
        // missing, so we need to validate the directory SOMEHOW.
        if let None = remote {
            if !is_git_repository(&mut path)? {
                return Err(ConfigError::UnknownRemoteError(path));
            }
        }

        let name = if let Some(name) = name {
            name.clone()
        } else {
            // TODO: camino! lol!
            path.file_name()
                .ok_or(ConfigError::RepositoryNameError(format!("{:?}", path)))?
                .to_str()
                .ok_or(ConfigError::RepositoryNameError(format!("{:?}", path)))?
                .to_string()
        };

        let name = self.unique_name(&name)?;
        let remote = if let Some(remote) = remote {
            Some(remote.clone())
        } else {
            git_remote(&path)?
        };
        // TODO: camino lol
        let path = path
            .into_os_string()
            .into_string()
            .map_err(|e| ConfigError::OsStringError(e))?;

        Ok(Repository { name, remote, path })
    }

    pub(crate) fn insert(
        &mut self,
        repository: Repository,
    ) -> Result<(usize, Repository), ConfigError> {
        for repo in &self.config.repositories {
            if repo.path == repository.path {
                return Err(ConfigError::UniqueRepositoryError(
                    repo.name.clone(),
                    repo.path.clone(),
                ));
            }
        }

        self.config.repositories.push(repository.clone());
        self.config.save()?;

        Ok((self.config.repositories.len() - 1, repository))
    }

    // TODO: expose these in the CLI
    pub(crate) fn get(&self, index: usize) -> Option<Repository> {
        self.config.repositories.get(index).map(|r| r.clone())
    }

    pub(crate) fn replace(
        &mut self,
        index: usize,
        repository: Repository,
    ) -> Result<(usize, Repository), ConfigError> {
        self.delete(index)?;
        self.config.repositories.insert(index, repository.clone());
        self.config.save()?;
        Ok((index, repository))
    }

    pub(crate) fn delete(&mut self, index: usize) -> Result<(), ConfigError> {
        self.config.repositories.remove(index);
        self.config.save()?;
        Ok(())
    }

    pub(crate) fn find(
        &self,
        selector: &Option<String>,
    ) -> Result<(usize, Repository), ConfigError> {
        let index = self.find_index(selector)?;
        let repo = self
            .get(index)
            .ok_or(ConfigError::RepositoryNotFoundError(index))?;
        Ok((index, repo))
    }

    pub(crate) fn find_index(&self, selector: &Option<String>) -> Result<usize, ConfigError> {
        // if no selector, default to the current directory
        let selector = if let Some(selector) = selector {
            selector.clone()
        } else {
            env::current_dir()?
                .into_os_string()
                .into_string()
                .map_err(|e| ConfigError::OsStringError(e))?
        };

        let index: usize = selector.parse().or_else(|_| {
            self.config
                .repositories
                .iter()
                .position(|repo| repo.name == selector || repo.path == selector)
                .ok_or(ConfigError::RepositorySearchError(selector))
        })?;

        Ok(index)
    }
}
