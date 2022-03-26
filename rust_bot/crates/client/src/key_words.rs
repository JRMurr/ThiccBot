use core::fmt;

use serde::{Deserialize, Serialize};

use crate::{error::ThiccError, ThiccClient, ThiccResult};

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyWord {
    pub name: String,
    pub responses: Vec<String>,
    pub match_case: bool,
}

impl From<(String, String)> for KeyWord {
    fn from((name, response): (String, String)) -> Self {
        Self {
            name,
            responses: vec![response],
            match_case: false,
        }
    }
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

impl fmt::Display for KeyWord {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}

pub struct KeyWordManager<'a> {
    client: &'a ThiccClient,
    guild_route: String,
}

impl KeyWordManager<'_> {
    pub async fn get(&self, search: &str) -> ThiccResult<Option<KeyWord>> {
        let res = self
            .client
            .get_json(format!("{}/{}", self.guild_route, search))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn list(&self) -> ThiccResult<Vec<KeyWord>> {
        self.client.get_json(&self.guild_route).await
    }

    pub async fn create(&self, key_word: &KeyWord) -> ThiccResult<KeyWord> {
        let res = self.client.post_json(&self.guild_route, key_word).await;
        ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::BAD_REQUEST {
                Some(ThiccError::ResourceAlreadyExist {
                    name: key_word.name.clone(),
                    resource_type: "Key Word".to_string(),
                })
            } else {
                None
            }
        })
    }

    pub async fn update(&self, key_word: &KeyWord) -> ThiccResult<KeyWord> {
        let res = self.client.put_json(
            format!("{}/{}", &self.guild_route, key_word.name),
            key_word
        ).await;
        ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::BAD_REQUEST {
                Some(ThiccError::ResourceAlreadyExist {
                    name: key_word.name.clone(),
                    resource_type: "Key Word".to_string(),
                })
            } else {
                None
            }
        })
    }

    pub async fn delete(&self, key_word: &str) -> ThiccResult<()> {
        self.client
            .delete_helper(format!("{}/{}", self.guild_route, key_word))
            .await
    }
}

const KEY_WORDS_ROUTE: &str = "keyWords/discord";

impl ThiccClient {
    pub fn key_words(&self, guild_id: u64) -> KeyWordManager {
        let guild_route = format!("{}/{}", KEY_WORDS_ROUTE, guild_id);
        KeyWordManager {
            client: self,
            guild_route,
        }
    }
}
