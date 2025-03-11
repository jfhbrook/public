use anyhow::Result;
use config::Config;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub(crate) struct Lockfile {}

pub(crate) fn get_lockfile() -> Result<Lockfile> {
    let cfg = Config::builder()
        .add_source(config::File::with_name("nopkg.lock.toml"))
        .build()?;

    let lockfile = cfg.try_deserialize::<Lockfile>()?;

    Ok(lockfile)
}
