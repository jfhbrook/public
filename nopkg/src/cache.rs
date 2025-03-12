use anyhow::Result;
use sha3::{Digest, Sha3_256};
use xdg::BaseDirectories;

// ~/.local/cache/files
// ~/.local/cache/repos
// ~/.local/cache/unpacked
pub(crate) fn get_cache() -> Result<Cache> {
    let dirs = BaseDirectories::with_prefix("nopkg")?;
    Ok(Cache { dirs })
}

struct Cache {
    dirs: BaseDirectories,
}

// TODO: hash for address
// TODO: file download
// TODO: git clone
// TODO: git checkout
// TODO: git pull
// TODO: tar unpack
// TODO: zip unpack
