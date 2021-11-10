use anyhow::Result;
use serde::{Deserialize, Serialize};

use crate::ThiccClient;

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyWord {
    name: String,
    pub responses: Vec<String>,
    match_case: bool,
}

impl KeyWord {
    pub fn new<NameStr, ResponseStr>(
        name: NameStr,
        responses: Vec<ResponseStr>,
    ) -> Self
    where
        NameStr: Into<String>,
        Vec<String>: From<Vec<ResponseStr>>,
    {
        Self {
            name: name.into(),
            responses: responses.into(),
            match_case: false,
        }
    }
}

pub struct KeyWordManager<'a> {
    client: &'a ThiccClient,
}

impl KeyWordManager<'_> {
    pub async fn get(
        &self,
        guild_id: u64,
        search: &str,
    ) -> Result<Option<KeyWord>> {
        let res = self
            .client
            .get_json::<KeyWord>(&format!(
                "keyWords/discord/{}/{}",
                guild_id, search
            ))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn create(
        &self,
        guild_id: u64,
        key_word: &KeyWord,
    ) -> Result<KeyWord> {
        self.client
            .post_json(&format!("keywords/discord/{}", guild_id), key_word)
            .await
    }
}

impl ThiccClient {
    pub fn key_words(&self) -> KeyWordManager {
        KeyWordManager { client: &self }
    }
}
