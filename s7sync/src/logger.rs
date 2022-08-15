use simplelog::{ColorChoice, Config, LevelFilter, TermLogger, TerminalMode};

pub(crate) fn init_logger() -> Result<(), log::SetLoggerError> {
    TermLogger::init(
        LevelFilter::Info,
        Config::default(),
        TerminalMode::Mixed,
        ColorChoice::Auto,
    )
}
