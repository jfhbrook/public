use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use anyhow::Result;
use refinery::embed_migrations;
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
        let mut db = Connection::open(&path)?;

        migrations::runner().run(&mut db)?;

        Ok(Index { path, db })
    }

    pub(crate) fn add_file(&mut self, url: &str) -> Result<()> {
        let id = get_id(url)?;
        let duration = SystemTime::now().duration_since(UNIX_EPOCH)?;
        let timestamp = duration.as_secs();

        self.db.execute(
            "insert into files (url, id, modified_at) values (?1, ?2, ?3) \
            on conflict(id) do update set url = ?1, modified_at = ?2",
            (url, &id, &timestamp),
        )?;

        Ok(())
    }
}

embed_migrations!("src/cache/migrations");
