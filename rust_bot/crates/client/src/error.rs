use thiserror::Error;

/// Generic error type for stuff that can go wrong making api errors
#[derive(Debug, Error, Clone)] // TODO: see if i can mess with the collection in handle_status so i don't need
                               // clone
pub enum ThiccError {
    #[error("{entity_type} with name {name} already exists")]
    NameAlreadyExist { entity_type: String, name: String },
}
