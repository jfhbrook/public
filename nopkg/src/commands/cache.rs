use anyhow::Result;
use chrono::{DateTime, Local};
use tabled::{builder::Builder, settings::Style};

use crate::cache::index::map_entry;
use crate::cache::{Cache, get_file, remove_file};

pub(crate) async fn cache_add_command(url: &String) -> Result<()> {
    let mut cache = Cache::new()?;
    get_file(&mut cache, url).await?;
    Ok(())
}

pub(crate) fn cache_remove_command(url: &String) -> Result<()> {
    let mut cache = Cache::new()?;
    remove_file(&mut cache, url)?;
    Ok(())
}

pub(crate) fn cache_destroy_command() -> Result<()> {
    let cache = Cache::new()?;
    cache.destroy()?;
    Ok(())
}

pub(crate) fn cache_show_command() -> Result<()> {
    let cache: Cache = Cache::new()?;

    let mut stmt = cache.index.entries()?;

    let entries = stmt.query_map([], map_entry)?;

    let mut root_builder = Builder::default();

    root_builder.push_record(["cache entries"]);

    let mut seen = false;

    for entry in entries {
        seen = true;
        let entry = entry?;

        // TODO: Flag for when to do this conversion
        let modified_at: DateTime<Local> = DateTime::from(entry.modified_at);
        let modified_at = modified_at.to_string();

        let mut entry_builder = Builder::default();
        entry_builder.push_record(["property", "value"]);
        entry_builder.push_record(["url", entry.url.as_str()]);
        entry_builder.push_record(["id", entry.id.as_str()]);
        entry_builder.push_record(["modified_at", modified_at.as_str()]);

        let mut entry_table = entry_builder.build();
        entry_table.with(Style::rounded());

        root_builder.push_record([format!("{}", entry_table)]);
    }

    if !seen {
        root_builder.push_record(["(the cache is empty)"]);
    }

    let mut root_table = root_builder.build();
    root_table.with(Style::rounded());

    println!("{}", root_table);

    Ok(())
}
