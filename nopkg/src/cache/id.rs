use anyhow::Result;
use sha3::{Digest, Sha3_256};
use tracing::trace;

pub(crate) fn get_id(url: &str) -> Result<String> {
    let mut hasher = Sha3_256::new();
    hasher.update(url);
    let hash = hasher.finalize();
    let hash = std::str::from_utf8(&hash)?;
    let hash = hash.to_string();

    trace!("{} -> {}", url, hash);

    Ok(hash)
}
