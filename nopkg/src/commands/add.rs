use anyhow::Result;
use camino::Utf8Path;

use crate::manifest::{Manifest, get_manifest};

pub(crate) fn add_command(
    url: &String,
    file: &Option<String>,
    unpack: &bool,
    manifest_path: &String,
) -> Result<()> {
    let manifest_path = Utf8Path::new(manifest_path);
    let manifest = get_manifest(manifest_path)?;
    println!("url: {}", url);
    println!("file: {:?}", file);
    println!("unpack: {}", unpack);
    // TODO: Load mut manifest
    // TODO: Append dependency to manifest
    // TODO: Write manifest to file
    unimplemented!("add file");
    Ok(())
}
