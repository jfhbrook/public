use clap::ValueEnum;
use tracing_subscriber::filter::LevelFilter;

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
pub(crate) enum LogLevel {
    Trace,
    Debug,
    Info,
    Warn,
    Error,
    Off,
}

impl Into<LevelFilter> for &LogLevel {
    fn into(self) -> LevelFilter {
        match self {
            LogLevel::Trace => LevelFilter::TRACE,
            LogLevel::Debug => LevelFilter::DEBUG,
            LogLevel::Info => LevelFilter::INFO,
            LogLevel::Warn => LevelFilter::WARN,
            LogLevel::Error => LevelFilter::ERROR,
            LogLevel::Off => LevelFilter::OFF,
        }
    }
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
pub(crate) enum LogFormat {
    Full,
    Compact,
    Pretty,
    Json,
}

pub(crate) fn configure_logging(level: &LogLevel, format: &LogFormat) -> () {
    let fmt = tracing_subscriber::fmt().with_max_level(level);

    match format {
        LogFormat::Full => {
            fmt.init();
        }
        LogFormat::Compact => {
            fmt.compact().init();
        }
        LogFormat::Pretty => {
            fmt.pretty().init();
        }
        LogFormat::Json => {
            fmt.json().init();
        }
    };
}
