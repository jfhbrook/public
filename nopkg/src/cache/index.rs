use std::path::PathBuf;

use anyhow::Result;
use rusqlite::Connection;
use tracing::trace;
use xdg::BaseDirectories;

use crate::cache::id::get_id;

/// Get the path to the index, and create any needed directories.
fn place_index(dirs: &BaseDirectories) -> Result<PathBuf> {
    let path = dirs.place_cache_file("index.json")?;

    trace!("Placing index at {:?}", path);

    Ok(path)
}

pub(crate) struct Index {
    path: PathBuf,
    db: Connection,
}

impl Index {
    pub(crate) fn new(dirs: &BaseDirectories) -> Result<Self> {
        let path = place_index(dirs)?;
        let db = Connection::open(&path)?;
        Ok(Index { path, db })
    }

    pub(crate) fn update(&mut self, url: &str) -> Result<()> {
        let hash = get_id(url)?;

        Ok(())
    }
}
