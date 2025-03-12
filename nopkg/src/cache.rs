use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use anyhow::{bail, Result};
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

pub(crate) struct Cache {
    dirs: BaseDirectories,
    index: CacheIndex,
}

impl Cache {
    pub(crate) fn new() -> Result<Self> {
        let dirs = BaseDirectories::with_prefix("nopkg")?;
        let index_path = dirs.place_cache_file("index.json")?;

        let index = read_index(&index_path)?;
        Ok(Cache { dirs, index })
    }

    pub(crate) fn place_file(&self, url: &String) -> Result<PathBuf> {
        let mut hasher = Sha3_256::new();
        hasher.update(url);
        let hash = hasher.finalize();
        let hash = std::str::from_utf8(&hash)?;

        let path = format!("file/{}", hash);
        let path = Utf8Path::new(&path);

        let path = self.dirs.place_cache_file(path)?;
        Ok(path)
    }
}

// TODO: load/save to index
// TODO: file download
// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
