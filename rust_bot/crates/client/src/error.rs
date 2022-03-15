use thiserror::Error;

#[derive(Debug, Error)]
/// Global Error for anything in this crate
pub enum ClientErrors {
    #[error("Invalid Relative url, should not start with a '/': {0}")]
    InvalidRelativeUrl(String),

    #[error(transparent)]
    Thicc(#[from] ThiccError),

    #[error(transparent)]
    Reqwest(#[from] reqwest::Error),

    #[error(transparent)]
    IoError(#[from] std::io::Error),

    #[error(transparent)]
    Other(#[from] anyhow::Error),

    #[error("Error parsing: {0}")]
    StrumParseError(#[from] strum::ParseError),
}

/// Errors that we should show the user
#[derive(Debug, Error)]
pub enum ThiccError {
    #[error("{resource_type} with name {name} already exists")]
    ResourceAlreadyExist { resource_type: String, name: String },

    #[error("Parse error: got {got}, allowed values: {allowed:?}")]
    ParseError {
        allowed: &'static [&'static str],
        got: String,
    },
}
