use anyhow::Result;

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
    Ok(())
}
