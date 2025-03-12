use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use anyhow::Result;
use camino::Utf8Path;
use serde_json::Value;
use sha3::{Digest, Sha3_256};
use xdg::BaseDirectories;

// ~/.local/cache/files
// ~/.local/cache/repos
// ~/.local/cache/unpacked

type CacheIndex = HashMap<String, String>;

fn read_index<P: AsRef<Path>>(path: P) -> Result<CacheIndex> {
    let path = path.as_ref();

    if !path.is_file() {
        return Ok(HashMap::new());
    }

    let file = fs::File::open(path)?;
    let reader = io::BufReader::new(file);

    let index: CacheIndex = serde_json::from_reader(reader)?;

    Ok(index)
}

fn write_index<P: AsRef<Path>>(path: P, index: &CacheIndex) -> Result<()> {
    let file = fs::File::open(path)?;
    let writer = io::BufWriter::new(file);

    serde_json::to_writer_pretty(writer, index)?;

    Ok(())
}

fn cache_path(dirs: &BaseDirectories) -> Result<PathBuf> {
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

pub(crate) struct Cache {
    dirs: BaseDirectories,
    index: CacheIndex,
}

impl Cache {
    pub(crate) fn new() -> Result<Self> {
        let dirs = BaseDirectories::with_prefix("nopkg")?;
        let path = cache_path(&dirs)?;

        let index = read_index(&path)?;
        Ok(Cache { dirs, index })
    }

    pub(crate) fn place_file(&self, url: &String) -> Result<PathBuf> {
        let path = file_path(url)?;
        let path = self.dirs.place_cache_file(path)?;
        Ok(path)
    }

    fn update_index(&mut self, url: &String) -> Result<()> {
        let hash = hash_url(url)?;
        let path = cache_path(&self.dirs)?;

        self.index.insert(url.clone(), hash);
        write_index(path, &self.index)?;

        Ok(())
    }
}

// TODO: load/save to index
// TODO: file download
// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
