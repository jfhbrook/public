use anyhow::Result;
use config::Config;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub(crate) struct Manifest {}

pub(crate) fn get_manifest() -> Result<Manifest> {
    let cfg = Config::builder()
        .add_source(config::File::with_name("nopkg.toml"))
        .build()?;

    let manifest = cfg.try_deserialize::<Manifest>()?;

    Ok(manifest)
}
