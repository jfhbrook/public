use anyhow::{Error, Result};
use log::{debug, info};
use tabled::{Table, Tabled};

use crate::data::{Config, Repositories, Repository};
use crate::logger::init_logger;

#[derive(Tabled)]
struct RepositoryView<'t> {
    index: usize,
    name: &'t str,
    path: &'t str,
    remote: &'t str,
}

fn map_view<'c>((index, repository): (usize, &'c Repository)) -> RepositoryView<'c> {
    let name: &'c str = repository.name.as_str();
    let path: &'c str = repository.path.as_str();
    let remote: &'c str = if let Some(remote) = &repository.remote {
        remote.as_str()
    } else {
        "<not set>"
    };

    RepositoryView::<'c> {
        index,
        name,
        path,
        remote,
    }
}

// Show all the repositories.
// TODO: Single-entity drill-down? Status? etc
pub(crate) fn show_command() -> Result<(), Error> {
    let config = Config::load()?;

    // TODO: impl custom Debug trait for config.repositories
    let repositories = config.repositories.iter().enumerate().map(map_view);

    println!("{}", Table::new(repositories).to_string());

    Ok(())
}

// Add a repository.
pub(crate) fn add_command(
    path: Option<String>,
    name: Option<String>,
    remote: Option<String>,
) -> Result<(), Error> {
    init_logger()?;

    // TODO: move to shared controller
    let mut config = Config::load()?;

    debug!("Current configuration:\n\n{config:#?}", config = config);

    let mut repos = Repositories::new(&mut config);

    let repo = repos.create(&path, &name, &remote)?;

    debug!("Inserting repository: {:?}", repo);

    repos.insert(repo)?;

    debug!("Updated configuration:\n\n{config:#?}", config = config);

    Ok(())
}

// Remove a repository.
pub(crate) fn remove_command(selector: Option<String>) -> Result<(), Error> {
    init_logger()?;

    // TODO: move to a shared controller
    let mut config = Config::load()?;

    debug!("Current configuration:\n\n{config:#?}", config = config);

    let mut repos = Repositories::new(&mut config);

    debug!("Searching for repository matching: {:?}", selector);

    let index = repos.find_index(&selector)?;

    info!("Deleting repository {index}", index = index);

    repos.delete(index)?;

    debug!("Updated configuration:\n\n{config:#?}", config = config);

    Ok(())
}

// TODO: Update, find one or >1, etc
