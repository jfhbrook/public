use std::io::Result;
use std::process::Command;

fn main() -> Result<()> {
    // TODO: gracefully fail if org-tangle isn't available
    let status = Command::new("org-tangle").arg("elisp.org").status()?;
    if status.success() {
        Ok(())
    } else {
        println!("warning, org-tangle exited with code {:?}", status);
        println!("it is likely the .el source has not been generated!");
        println!("open elisp.org in emacs and run C-c C-v C-t to update!");
        Ok(())
    }
}
