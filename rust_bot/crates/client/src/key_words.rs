use std::collections::HashMap;

use anyhow::Result;
use serde::{Deserialize, Serialize};

use crate::{error::ThiccError, ErrorMap, ThiccClient};

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyWord {
    pub name: String,
    pub responses: Vec<String>,
    pub match_case: bool,
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
    guild_route: String,
}

impl KeyWordManager<'_> {
    pub async fn get(&self, search: &str) -> Result<Option<KeyWord>> {
        let res = self
            .client
            .get_json::<KeyWord>(&format!("{}/{}", self.guild_route, search))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn list(&self) -> Result<Vec<KeyWord>> {
        self.client
            .get_json::<Vec<KeyWord>>(&self.guild_route)
            .await
    }

    pub async fn create(&self, key_word: &KeyWord) -> Result<KeyWord> {
        let errors: ErrorMap = HashMap::from([(
            reqwest::StatusCode::BAD_REQUEST,
            ThiccError::NameAlreadyExist {
                name: key_word.name.clone(),
                entity_type: "Key Word".to_string(),
            },
        )]);
        let res = self.client.post_json(&self.guild_route, key_word).await;
        ThiccClient::handle_status(res, errors)
    }
}

const KEY_WORDS_ROUTE: &str = "keyWords/discord";

impl ThiccClient {
    pub fn key_words(&self, guild_id: u64) -> KeyWordManager {
        let guild_route = format!("{}/{}", KEY_WORDS_ROUTE, guild_id);
        KeyWordManager {
            client: &self,
            guild_route,
        }
    }
}
