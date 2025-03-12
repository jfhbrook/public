use anyhow::Result;
use camino::Utf8Path;

use crate::init::init_manifest;
use crate::manifest::manifest_path;

pub(crate) fn init_command(path: &String, overwrite: bool) -> Result<()> {
    let path = Utf8Path::new(path);
    let path = manifest_path(path);
    init_manifest(path, overwrite)
}
