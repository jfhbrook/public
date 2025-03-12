use anyhow::Result;
use url;

#[derive(Debug)]
pub(crate) struct Url {}

impl Url {
    fn new() -> Self {
        Url {}
    }
}

pub(crate) fn parse_url(url: &str) -> Result<Url> {
    let url = url::Url::parse(url)?;
    println!("scheme: {}", url.scheme());
    Ok(Url::new())
}
