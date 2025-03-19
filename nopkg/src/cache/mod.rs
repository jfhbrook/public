use std::path::{Path, PathBuf};
use tracing::trace;

use anyhow::{Result, bail};
use xdg::BaseDirectories;

mod download;
mod id;
mod index;

use crate::cache::download::download_file;
use crate::cache::id::get_id;
use crate::cache::index::Index;

fn file_path(url: &str) -> Result<PathBuf> {
    let id = get_id(url)?;

    let path = format!("file/{}", id.as_str());
    let path = Path::new(&path);

    Ok(path.to_path_buf())
}

/*
fn unpacked_file_path(url: &str, path: &str) -> Result<PathBuf> {
    let id = get_id(url)?;

    let path = format!("unpacked/{}/{}", id, path);
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}
*/

fn repo_path(url: &str) -> Result<PathBuf> {
    let id = get_id(url)?;

    let path = format!("repos/{}", id);
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}

pub(crate) struct Cache {
    dirs: BaseDirectories,
    index: Index,
}

///
/// A resource cache. Handles flat files, unpacked archives and git repos.
///
impl Cache {
    /// Create a new resource cache.
    pub(crate) fn new() -> Result<Self> {
        let dirs = BaseDirectories::with_prefix("nopkg")?;
        let index = Index::new(&dirs)?;
        Ok(Cache { dirs, index })
    }

    // TODO: Should these take &str?
    pub(crate) fn place_file(&self, url: &str) -> Result<PathBuf> {
        let path = file_path(url)?;
        let path = self.dirs.place_cache_file(path)?;

        trace!("Placing {} at {:?}", url, path);

        Ok(path)
    }

    /*
    pub(crate) fn place_unpacked_file(&self, url: &str, path: &str) -> Result<PathBuf> {
        let unpacked_path = unpacked_file_path(url, path)?;
        let unpacked_path = self.dirs.place_cache_file(unpacked_path)?;

        trace!("Placing {} from {} at {:?}", path, url, unpacked_path);

        Ok(unpacked_path)
    }
    */
}

pub(crate) async fn get_file(cache: &mut Cache, url: &str) -> Result<PathBuf> {
    let path = cache.place_file(url)?;

    if path.is_file() {
        trace!("File {:?} already downloaded", path);
        return Ok(path);
    }

    if path.exists() {
        bail!("Entity at path exists but is not a file");
    }

    download_file(url, &path).await?;

    cache.index.add_file(url)?;

    Ok(path)
}

// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
