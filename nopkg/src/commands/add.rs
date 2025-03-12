use std::fs;

use anyhow::Result;
use camino::Utf8Path;
use toml;

use crate::manifest::{Dependency, get_manifest};

pub(crate) fn add_command(
    url: &String,
    file: &Option<String>,
    unpack: &bool,
    manifest_path: &String,
) -> Result<()> {
    let manifest_path = Utf8Path::new(manifest_path);
    let mut manifest = get_manifest(manifest_path)?;

    let mut dependencies = manifest.dependencies.unwrap_or(vec![]);

    dependencies.push(Dependency {
        name: None,
        url: url.clone(),
        file: file.clone(),
        unpack: Some(*unpack),
    });

    manifest.dependencies = Some(dependencies);

    let manifest = toml::to_string(&manifest)?;

    fs::write(manifest_path, manifest)?;

    Ok(())
}
