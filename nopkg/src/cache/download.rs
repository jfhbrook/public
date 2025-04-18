use std::cmp::min;
use std::fs::{File, remove_file};
use std::io::Write;
use std::path::Path;

use anyhow::{Result, anyhow};
use futures_util::StreamExt;
use indicatif::{ProgressBar, ProgressState, ProgressStyle};
use reqwest;
use tracing::debug;

fn rm_f(path: &Path) -> () {
    let res = remove_file(path);

    if let Err(err) = res {
        debug!("{:?}", err);
    };
}

// TODO: Customize
fn progress_bar(total_size: u64) -> ProgressBar {
    let bar = ProgressBar::new(total_size);

    let style = ProgressStyle::with_template(
        "{spinner:.green} [{elapsed_precise}] [{wide_bar:.cyan/blue}] {bytes}/{total_bytes} ({eta})"
    ).unwrap();
    let style = style.with_key(
        "eta",
        |state: &ProgressState, w: &mut dyn std::fmt::Write| {
            write!(w, "{:.1}s", state.eta().as_secs_f64()).unwrap()
        },
    );
    let style = style.progress_chars("#>-");

    bar.set_style(style);

    bar
}

pub(crate) async fn download_file<P: AsRef<Path>>(url: &str, path: P) -> Result<()> {
    let path = path.as_ref();
    let res = _download_file(url, path).await;

    if !res.is_ok() {
        rm_f(path);
    }

    res?;

    Ok(())
}

// See: https://gist.github.com/Tapanhaz/096e299bf060607b572d700e89a62529
async fn _download_file(url: &str, path: &Path) -> Result<()> {
    let res = reqwest::get(url).await?;

    // TODO: Gracefully handle when total size is unknown?
    let total_size = res.content_length().unwrap_or(1024);

    let bar = progress_bar(total_size);
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
