use std::io;

use anyhow::Result;
use clap::Command;
use clap_complete::aot::{Shell, generate};

// TODO: https://docs.rs/clap_complete/latest/clap_complete/
pub(crate) fn completion_command(shell: Option<Shell>, command: &mut Command) -> Result<()> {
    let generator = shell.unwrap_or(Shell::Bash);
    generate(
        generator,
        command,
        command.get_name().to_string(),
        &mut io::stdout(),
    );
    Ok(())
}
