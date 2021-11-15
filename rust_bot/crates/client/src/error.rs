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
    Other(#[from] anyhow::Error),
}

/// Errors that we should show the user
#[derive(Debug, Error)]
pub enum ThiccError {
    #[error("{resource_type} with name {name} already exists")]
    ResourceAlreadyExist { resource_type: String, name: String },
}
