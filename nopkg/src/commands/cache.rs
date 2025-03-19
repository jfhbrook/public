use anyhow::Result;
use tabled::Table;
use tabled::settings::Style;

use crate::cache::index::{Entry, map_entry};
use crate::cache::{Cache, get_file};

pub(crate) async fn cache_add_command(url: &String) -> Result<()> {
    let mut cache = Cache::new()?;
    get_file(&mut cache, url).await?;
    Ok(())
}

pub(crate) fn cache_clean_command() -> Result<()> {
    Ok(())
}

pub(crate) fn cache_show_command() -> Result<()> {
    let cache: Cache = Cache::new()?;

    let mut stmt = cache.index.entries()?;

    let entries = stmt.query_map([], map_entry)?;
    let entries: std::result::Result<Vec<Entry>, rusqlite::Error> = entries.collect();
    let entries = entries?;

    let mut table = Table::new(entries);
    table.with(Style::modern());

    println!("{}", table);

    Ok(())
}
