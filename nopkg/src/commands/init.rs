use anyhow::Result;
use camino::{Utf8Path, Utf8PathBuf};

use crate::init::init_manifest;

fn full_path(path: &Utf8Path) -> Utf8PathBuf {
    match path.extension() {
        Some(ext) if ext == "toml" => path.to_path_buf(),
        _ => {
            let mut buf = path.to_path_buf();
            buf.push("unpkg.toml");
            buf
        }
    }
}

pub(crate) fn init_command(path: &Option<String>, overwrite: bool) -> Result<()> {
    let path = path.clone().unwrap_or("./unpkg.toml".to_string());
    let path = Utf8Path::new(&path);
    let path = full_path(path);
    init_manifest(path.as_path(), overwrite)
}
