use anyhow::Result;
use serde::{Deserialize, Serialize};

use crate::ThiccClient;

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyWord {
    name: String,
    responses: Vec<String>,
    match_case: bool,
}

impl ThiccClient {
    pub async fn get_key_words(
        &self,
        server_id: &str,
        search: &str,
    ) -> Result<Vec<KeyWord>> {
        let res = self
            .get(&format!("keyWords/discord/{}/{}", server_id, search))?
            .send()
            .await?
            .error_for_status()? // TODO: instead of this match and don't throw error if 404
            .json()
            .await?;

        Ok(res)
    }
}
