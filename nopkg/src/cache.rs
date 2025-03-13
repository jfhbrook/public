use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use anyhow::Result;
use sha3::{Digest, Sha3_256};
use xdg::BaseDirectories;

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
    Ok(path)
}

fn hash_url(url: &String) -> Result<String> {
    let mut hasher = Sha3_256::new();
    hasher.update(url);
    let hash = hasher.finalize();
    let hash = std::str::from_utf8(&hash)?;
    Ok(hash.to_string())
}

fn file_path(url: &String) -> Result<PathBuf> {
    let hash = hash_url(url)?;

    let path = format!("file/{}", hash.as_str());
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}

fn unpacked_file_path(url: &String, path: &String) -> Result<PathBuf> {
    let hash = hash_url(url)?;

    let path = format!("unpacked/{}/{}", hash, path);
    let path = Path::new(&path);
    Ok(path.to_path_buf())
}

fn repo_path(url: &String) -> Result<PathBuf> {
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
    pub(crate) fn place_file(&self, url: &String) -> Result<PathBuf> {
        let path = file_path(url)?;
        let path = self.dirs.place_cache_file(path)?;
        Ok(path)
    }

    pub(crate) fn place_unpacked_file(&self, url: &String, path: &String) -> Result<PathBuf> {
        let path = unpacked_file_path(url, path)?;
        let path = self.dirs.place_cache_file(path)?;
        Ok(path)
    }

    pub(crate) fn update_index(&mut self, url: &String) -> Result<()> {
        let hash = hash_url(url)?;
        let path = place_index(&self.dirs)?;

        self.index.insert(url.clone(), hash);
        write_index(path, &self.index)?;

        Ok(())
    }

    pub(crate) fn open_file(&self, url: &String) -> Result<fs::File> {
        let path = self.place_file(url)?;
        let file = fs::File::open(path)?;
        Ok(file)
    }

    pub(crate) fn open_unpacked_file(&self, url: &String, path: &String) -> Result<fs::File> {
        let path = self.place_unpacked_file(url, path)?;
        let file = fs::File::open(path)?;
        Ok(file)
    }
}

// TODO: file download
// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
