use std::fs;

use anyhow::{Result, bail};
use camino::Utf8Path;

const TEMPLATE: &str = include_str!("./nopkg.toml");

pub(crate) fn init_manifest<P: AsRef<Utf8Path>>(path: P, overwrite: bool) -> Result<()> {
    let path = path.as_ref();
    if (!overwrite && path.is_file()) {
        bail!("Cowardly refusing to overwrite {}", path);
    }

    fs::write(path, TEMPLATE)?;

    Ok(())
}
