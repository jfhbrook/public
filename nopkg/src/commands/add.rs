use anyhow::Result;
use camino::Utf8Path;
use tracing::{debug, info_span};

use crate::manifest::{Dependency, get_manifest, write_manifest};

pub(crate) fn add_command(
    url: &String,
    file: &Option<String>,
    unpack: &bool,
    manifest_path: &String,
) -> Result<()> {
    info_span!("Adding dependency");
    debug!("url: {}", url);
    match file {
        Some(file) => {
            debug!("file: {}", file);
        }
        None => {}
    };
    debug!("unpack: {}", unpack);
    debug!("manifest: {}", manifest_path);

    let manifest_path = Utf8Path::new(manifest_path);
    let mut manifest = get_manifest(manifest_path)?;

    let mut dependencies = manifest.dependencies;
    // let mut dev_dependencies = manifest.dev_dependencies.unwrap_or(vec![]);

    // TODO: Handle file, unpack, etc
    dependencies.push(Dependency::Url(url.clone()));

    manifest.dependencies = dependencies;

    write_manifest(manifest_path, &manifest)?;

    Ok(())
}
