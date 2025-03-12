use anyhow::Result;
use camino::Utf8Path;
use config::Config;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub(crate) struct Lockfile {}

pub(crate) fn get_lockfile<P: AsRef<Utf8Path>>(path: P) -> Result<Lockfile> {
    let path = path.as_ref();

    let cfg = Config::builder()
        .add_source(config::File::with_name("nopkg.lock.toml"))
        .build()?;

    let lockfile = cfg.try_deserialize::<Lockfile>()?;

    Ok(lockfile)
}
