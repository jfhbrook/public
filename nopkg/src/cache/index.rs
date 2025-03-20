use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use anyhow::Result;
use chrono::{DateTime, Utc};
use refinery::embed_migrations;
use rusqlite::{Connection, Row, Statement};
use tracing::trace;
use xdg::BaseDirectories;

use crate::cache::id::get_id;

/// Get the path to the index, and create any needed directories.
fn place_index(dirs: &BaseDirectories) -> Result<PathBuf> {
    let path = dirs.place_cache_file("index.json")?;

    trace!("Placing index at {:?}", path);

    Ok(path)
}

pub(crate) struct Entry {
    pub(crate) url: String,
    pub(crate) id: String,
    pub(crate) modified_at: DateTime<Utc>,
}

fn new_timestamp() -> f64 {
    let duration = SystemTime::now().duration_since(UNIX_EPOCH).unwrap();
    let duration = duration.as_millis();
    (duration as f64) / 1000.0
}

fn from_timestamp(timestamp: f64) -> DateTime<Utc> {
    let timestamp = (timestamp * 1000.0) as i64;
    let modified_at = DateTime::from_timestamp_millis(timestamp);
    modified_at.unwrap()
}

pub(crate) fn map_entry(row: &Row) -> std::result::Result<Entry, rusqlite::Error> {
    let url = row.get(0)?;
    let id = row.get(1)?;
    let modified_at = from_timestamp(row.get(2)?);

    Ok(Entry {
        url,
        id,
        modified_at,
    })
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
        let modified_at = new_timestamp();

        self.db.execute(
            "insert into files (url, id, modified_at) values (?1, ?2, ?3) \
            on conflict(id) do update set url = ?1, modified_at = ?2",
            (url, &id, &modified_at),
        )?;

        Ok(())
    }

    pub(crate) fn entries(&self) -> Result<Statement> {
        let stmt = self.db.prepare("select url, id, modified_at from files;")?;
        Ok(stmt)
    }
}

embed_migrations!("src/cache/migrations");
