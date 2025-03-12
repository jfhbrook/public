use anyhow::Result;

pub(crate) fn add_file_command(url: &String, file: &Option<String>) -> Result<()> {
    println!("url: {}", url);
    if let Some(file) = file {
        println!("file: {}", file);
    }
    unimplemented!("add file");
    Ok(())
}

pub(crate) fn add_archive_command(url: &String) -> Result<()> {
    println!("url: {}", url);
    unimplemented!("add archive");
    Ok(())
}

pub(crate) fn add_repo_command(url: &String) -> Result<()> {
    println!("url: {}", url);
    unimplemented!("add repo");
    Ok(())
}
