use anyhow::Result;
use base64::{Engine as _, engine::general_purpose::URL_SAFE};
use sha3::{Digest, Sha3_256};
use tracing::trace;

pub(crate) fn get_id(url: &str) -> Result<String> {
    trace!("hashing {}", url);
    let mut hasher = Sha3_256::new();
    hasher.update(url);
    let hash = hasher.finalize();
    let hash = URL_SAFE.encode(&hash);

    trace!("{} -> {}", url, hash);

    Ok(hash)
}
