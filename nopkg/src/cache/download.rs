use std::cmp::min;
use std::fs::File;
use std::io::Write;
use std::path::Path;

use anyhow::{Result, anyhow};
use futures_util::StreamExt;
use indicatif::ProgressBar;
use reqwest::Client;

// See: https://gist.github.com/Tapanhaz/096e299bf060607b572d700e89a62529
pub(crate) async fn download_file<P: AsRef<Path>>(
    client: &Client,
    url: &str,
    path: P,
) -> Result<()> {
    let path = path.as_ref();
    let res = client.get(url).send().await?;

    // TODO: Gracefully handle when total size is unknown?
    let total_size = res
        .content_length()
        .ok_or(anyhow!("No content length specified"))?;

    // TODO: Customize style
    let bar = ProgressBar::new(total_size);
    let msg = format!("Downloading {}", url);
    bar.set_message(msg);

    let mut downloaded: u64 = 0;
    let mut stream = res.bytes_stream();

    let mut file = File::create(path).or(Err(anyhow!("Failed to create file")))?;

    while let Some(item) = stream.next().await {
        let chunk = item?;
        file.write_all(&chunk)?;
        downloaded = min(downloaded + (chunk.len() as u64), total_size);
        bar.set_position(downloaded);
    }

    Ok(())
}

// TODO: https://github.com/console-rs/indicatif/blob/HEAD/examples/yarnish.rs
