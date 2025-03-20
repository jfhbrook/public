use std::path::{Path, PathBuf};
use tracing::trace;

use anyhow::{Result, bail};
use xdg::BaseDirectories;

mod download;
mod id;
pub(crate) mod index;

use crate::cache::download::download_file;
use crate::cache::id::get_id;
use crate::cache::index::Index;

fn id_path(id: &str) -> Result<PathBuf> {
    let path = format!("file/{}", id);
    let path = Path::new(&path);

    Ok(path.to_path_buf())
}

fn url_path(url: &str) -> Result<PathBuf> {
    let id = get_id(url)?;
    let path = id_path(id.as_str())?;
    Ok(path)
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
    pub(crate) dirs: BaseDirectories,
    pub(crate) index: Index,
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

    pub(crate) fn destroy(&self) -> Result<()> {
        let path = self.dirs.get_cache_home();
        std::fs::remove_dir_all(path)?;
        Ok(())
    }

    pub(crate) fn place_file(&self, url: &str) -> Result<PathBuf> {
        let path = url_path(url)?;
        let path = self.dirs.place_cache_file(path)?;

        trace!("Placing {} at {:?}", url, path);

        Ok(path)
    }

    pub(crate) fn find_file(&self, url_or_id: &str) -> Result<Option<PathBuf>> {
        let path = self.find_file_by_id(url_or_id)?;

        if let Some(path) = path {
            return Ok(Some(path));
        }

        Ok(self.find_file_by_url(url_or_id)?)
    }

    pub(crate) fn find_file_by_id(&self, id: &str) -> Result<Option<PathBuf>> {
        let path = id_path(id)?;
        Ok(self.dirs.find_cache_file(path))
    }

    pub(crate) fn find_file_by_url(&self, url: &str) -> Result<Option<PathBuf>> {
        let path = url_path(url)?;
        Ok(self.dirs.find_cache_file(path))
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

pub(crate) fn remove_file(cache: &mut Cache, url_or_id: &str) -> Result<()> {
    let path = cache.find_file(url_or_id)?;

    if let Some(path) = path {
        std::fs::remove_file(path)?;
    }

    cache.index.remove_file(url_or_id)?;
    Ok(())
}

// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
