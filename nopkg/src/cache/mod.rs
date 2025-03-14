use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use tracing::trace;

use anyhow::{Result, bail};
use reqwest::Client;
use sha3::{Digest, Sha3_256};
use xdg::BaseDirectories;

mod download;

use crate::cache::download::download_file;

/// A map between URL and hash
type CacheIndex = HashMap<String, String>;

fn read_index<P: AsRef<Path>>(path: P) -> Result<CacheIndex> {
    /// Read an index file.
    let path = path.as_ref();

    if !path.is_file() {
        return Ok(HashMap::new());
    }

    let file = fs::File::open(path)?;
    let reader = io::BufReader::new(file);

    // TODO: Use SQLITE?
    let index: CacheIndex = serde_json::from_reader(reader)?;

    Ok(index)
}

fn write_index<P: AsRef<Path>>(path: P, index: &CacheIndex) -> Result<()> {
    /// Write out an index file.
    let file = fs::File::open(path)?;
    let writer = io::BufWriter::new(file);

    serde_json::to_writer_pretty(writer, index)?;

    Ok(())
}

fn place_index(dirs: &BaseDirectories) -> Result<PathBuf> {
    /// Get the path to the index, and create any needed directories.
    let path = dirs.place_cache_file("index.json")?;

    trace!("Placing index at {:?}", path);

    Ok(path)
}

fn hash_url(url: &str) -> Result<String> {
    let mut hasher = Sha3_256::new();
    hasher.update(url);
    let hash = hasher.finalize();
    let hash = std::str::from_utf8(&hash)?;
    let hash = hash.to_string();

    trace!("{} -> {}", url, hash);

    Ok(hash)
}

fn file_path(url: &str) -> Result<PathBuf> {
    let hash = hash_url(url)?;

    let path = format!("file/{}", hash.as_str());
    let path = Path::new(&path);

    Ok(path.to_path_buf())
}

fn unpacked_file_path(url: &str, path: &str) -> Result<PathBuf> {
    let hash = hash_url(url)?;

    let path = format!("unpacked/{}/{}", hash, path);
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}

fn repo_path(url: &str) -> Result<PathBuf> {
    let hash = hash_url(url)?;

    let path = format!("repos/{}", hash);
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}

pub(crate) struct Cache {
    dirs: BaseDirectories,
    index: CacheIndex,
}

impl Cache {
    ///
    /// A resource cache. Handles flat files, unpacked archives and git repos.
    ///

    pub(crate) fn new() -> Result<Self> {
        /// Create a new resource cache.
        let dirs = BaseDirectories::with_prefix("nopkg")?;
        let path = place_index(&dirs)?;

        let index = read_index(&path)?;
        Ok(Cache { dirs, index })
    }

    // TODO: Should these take &str?
    pub(crate) fn place_file(&self, url: &str) -> Result<PathBuf> {
        let path = file_path(url)?;
        let path = self.dirs.place_cache_file(path)?;

        trace!("Placing {} at {:?}", url, path);

        Ok(path)
    }

    pub(crate) fn place_unpacked_file(&self, url: &str, path: &str) -> Result<PathBuf> {
        let unpacked_path = unpacked_file_path(url, path)?;
        let unpacked_path = self.dirs.place_cache_file(unpacked_path)?;

        trace!("Placing {} from {} at {:?}", path, url, unpacked_path);

        Ok(unpacked_path)
    }

    pub(crate) fn update_index(&mut self, url: &str) -> Result<()> {
        let hash = hash_url(url)?;
        let path = place_index(&self.dirs)?;

        self.index.insert(url.to_string(), hash);
        write_index(path, &self.index)?;

        Ok(())
    }
}

pub(crate) async fn get_file(cache: &mut Cache, client: &Client, url: &str) -> Result<PathBuf> {
    let file = cache.place_file(url)?;

    if file.is_file() {
        return Ok(file);
    }

    if file.exists() {
        bail!("Entity at path exists but is not a file");
    }

    download_file(client, url, &file).await?;

    cache.update_index(url)?;

    Ok(file)
}

// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
