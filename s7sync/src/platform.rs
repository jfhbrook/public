#[derive(Debug)]
pub(crate) enum Platform {
    Windows,
    MacOs,
    Linux
}

#[cfg(target_os = "windows")]
pub(crate) fn get_platform() -> Platform {
    Platform::Windows
}

#[cfg(target_os = "macos")]
pub(crate) fn get_platform() -> Platform {
    Platform::MacOs
}

#[cfg(target_os = "linux")]
pub(crate) fn get_platform() -> Platform {
    Platform::Linux
}
