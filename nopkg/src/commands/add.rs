use anyhow::Result;

pub(crate) fn add_command(url: &String, file: &Option<String>, unpack: &bool) -> Result<()> {
    println!("url: {}", url);
    println!("file: {:?}", file);
    println!("unpack: {}", unpack);
    // TODO: Load mut manifest
    // TODO: Append dependency to manifest
    // TODO: Write manifest to file
    unimplemented!("add file");
    Ok(())
}
