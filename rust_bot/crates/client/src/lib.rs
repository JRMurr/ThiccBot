use anyhow::{Context, Result};
use reqwest::{
    header::{HeaderMap, HeaderValue, AUTHORIZATION},
    Client, RequestBuilder, Url,
};

pub mod guilds;
pub mod key_words;

/// Wrapper around [`Client`] to support a `base_url`
#[derive(Debug)]
pub struct ThiccClient {
    client: Client,
    base_url: Url,
}

impl ThiccClient {
    /// Makes a new [`ThiccClient`] with the provided `base_url` and `api_key`
    pub fn new(base_url: &str, api_key: &str) -> ThiccClient {
        let base_url = Url::parse(base_url).expect("Error parsing base url");

        let mut headers = HeaderMap::new();
        let mut auth_value = HeaderValue::from_str(api_key).expect("Error parsing api_key");
        auth_value.set_sensitive(true);
        headers.insert(AUTHORIZATION, auth_value);

        let client = Client::builder()
            .default_headers(headers)
            .build()
            .expect("Error building client");

        ThiccClient { client, base_url }
    }

    fn join_with_base(&self, url: &str) -> Result<Url> {
        let url = self
            .base_url
            .join(url)
            .with_context(|| format!("Failed parsing relative url {}", url))?;
        Ok(url)
    }

    pub fn post(&self, url: &str) -> Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.post(url))
    }

    pub fn get(&self, url: &str) -> Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.get(url))
    }

    pub fn delete(&self, url: &str) -> Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.delete(url))
    }
}
