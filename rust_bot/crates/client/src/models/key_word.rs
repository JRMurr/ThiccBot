use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyWord {
    name: String,
    responses: Vec<String>,
    match_case: bool,
}
