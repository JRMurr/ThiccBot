use core::fmt;

use serde::{Deserialize, Serialize};

use crate::{ThiccClient, ThiccResult};

const QUOTE_ROUTE: &str = "quotes/discord";

#[derive(Debug, Serialize)]
pub struct QuoteCreate {
    pub quote: String,
    pub author: String,
}

impl From<(String, String)> for QuoteCreate {
    fn from((quote, author): (String, String)) -> Self {
        Self { quote, author }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Quote {
    pub id: usize,
    pub quote: String,
    pub author: String,
}

impl fmt::Display for Quote {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "\"{}\" - {}", self.quote, self.author)
    }
}

pub struct QuoteManager<'a> {
    client: &'a ThiccClient,
    guild_route: String,
}

impl QuoteManager<'_> {
    pub async fn create(&self, quote: &QuoteCreate) -> ThiccResult<Quote> {
        self.client.post_json(&self.guild_route, quote).await
    }

    pub async fn search<S: Into<String>>(
        &self,
        search: S,
    ) -> ThiccResult<Option<Quote>> {
        let res = self
            .client
            .get_json(format!(
                "{}/random?=search{}",
                self.guild_route,
                search.into()
            ))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn list(&self) -> ThiccResult<Vec<Quote>> {
        self.client.get_json(&self.guild_route).await
    }

    pub async fn get_random(&self) -> ThiccResult<Option<Quote>> {
        let res = self
            .client
            .get_json(format!("{}/random", self.guild_route))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn delete(&self, quote_id: usize) -> ThiccResult<()> {
        self.client
            .delete_helper(format!("{}/{}", self.guild_route, quote_id))
            .await
    }
}

impl ThiccClient {
    pub fn quotes(&self, guild_id: u64) -> QuoteManager {
        let guild_route = format!("{}/{}", QUOTE_ROUTE, guild_id);
        QuoteManager {
            client: self,
            guild_route,
        }
    }
}
