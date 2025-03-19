use std::fs;

use anyhow::{Result, bail};
use camino::{Utf8Path, Utf8PathBuf};
use config::{Config, FileFormat};
use serde::{Deserialize, Serialize};
use serde_yaml;
use tracing::{debug, debug_span};

#[derive(Deserialize, Serialize)]
pub(crate) struct Manifest {
    pub(crate) dependencies: Vec<Dependency>,
    pub(crate) dev_dependencies: Option<Vec<Dependency>>,
}

#[derive(Deserialize, Serialize)]
pub(crate) enum Dependency {
    Url(String),
    Spec(Spec),
}

#[derive(Deserialize, Serialize)]
pub(crate) enum Spec {
    FileSpec { output: String },
    // TODO: DSL
    ArchiveSpec { unpack: Vec<String> },
}

const TEMPLATE: &str = include_str!("./nopkg.yaml");

pub(crate) fn manifest_path(path: &Utf8Path) -> Utf8PathBuf {
    let path = match path.extension() {
        Some(ext) if ext == "yaml" || ext == "yml" => path.to_path_buf(),
        _ => {
            let mut buf = path.to_path_buf();
            buf.push("nopkg.yaml");
            buf
        }
    };

    debug!("Expecting manifest at {}", path);

    path
}

pub(crate) fn get_manifest<P: AsRef<Utf8Path>>(path: P) -> Result<Manifest> {
    debug_span!("Loading manifest");

    let path = path.as_ref();
    let path = manifest_path(path);

    let cfg = Config::builder()
        .add_source(config::File::new(path.as_str(), FileFormat::Yaml))
        .build()?;

    let manifest = cfg.try_deserialize::<Manifest>()?;

    debug!("Manifest loaded.");

    Ok(manifest)
}

pub(crate) fn write_manifest<P: AsRef<Utf8Path>>(path: P, manifest: &Manifest) -> Result<()> {
    debug_span!("Writing manifest");

    let path = path.as_ref();
    let manifest = serde_yaml::to_string(manifest)?;

    fs::write(path, manifest)?;

    Ok(())
}

pub(crate) fn init_manifest<P: AsRef<Utf8Path>>(path: P, overwrite: bool) -> Result<()> {
    debug_span!("Initializing manifest");

    let path = path.as_ref();
    if !overwrite && path.is_file() {
        bail!("Cowardly refusing to overwrite {}", path);
    }

    fs::write(path, TEMPLATE)?;

    Ok(())
}
