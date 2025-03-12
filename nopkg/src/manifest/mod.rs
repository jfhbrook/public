use std::fs;

use anyhow::{Result, bail};
use camino::{Utf8Path, Utf8PathBuf};
use config::{Config, FileFormat};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub(crate) struct Manifest {
    dependencies: Vec<Dependency>,
}

#[derive(Deserialize, Serialize)]
pub(crate) struct Dependency {
    name: Option<String>,
    url: String,
    file: Option<String>,
    unpack: Option<bool>,
}

const TEMPLATE: &str = include_str!("./nopkg.toml");

pub(crate) fn manifest_path(path: &Utf8Path) -> Utf8PathBuf {
    match path.extension() {
        Some(ext) if ext == "toml" => path.to_path_buf(),
        _ => {
            let mut buf = path.to_path_buf();
            buf.push("unpkg.toml");
            buf
        }
    }
}

pub(crate) fn get_manifest<P: AsRef<Utf8Path>>(path: P) -> Result<Manifest> {
    let path = path.as_ref();
    let path = manifest_path(path);

    let cfg = Config::builder()
        .add_source(config::File::from_str(path.as_str(), FileFormat::Toml))
        .build()?;

    let manifest = cfg.try_deserialize::<Manifest>()?;

    Ok(manifest)
}

pub(crate) fn init_manifest<P: AsRef<Utf8Path>>(path: P, overwrite: bool) -> Result<()> {
    let path = path.as_ref();
    if !overwrite && path.is_file() {
        bail!("Cowardly refusing to overwrite {}", path);
    }

    fs::write(path, TEMPLATE)?;

    Ok(())
}
