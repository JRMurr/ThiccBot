use thiserror::Error;

/// Generic error type for stuff that can go wrong making api errors
#[derive(Debug, Error)]
pub enum ThiccError {
    #[error("{entity_type} with name {name} already exists")]
    NameAlreadyExist { entity_type: String, name: String },
}
