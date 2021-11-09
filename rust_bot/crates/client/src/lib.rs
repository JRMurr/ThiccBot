use anyhow::{Context, Result};
use reqwest::{
    header::{HeaderMap, HeaderValue, AUTHORIZATION},
    Client, RequestBuilder, Url,
};
use serde::{de::DeserializeOwned, Serialize};

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
        let mut auth_value =
            HeaderValue::from_str(api_key).expect("Error parsing api_key");
        auth_value.set_sensitive(true);
        headers.insert(AUTHORIZATION, auth_value);

        let client = Client::builder()
            .default_headers(headers)
            .build()
            .expect("Error building client");

        ThiccClient { client, base_url }
    }

    fn join_with_base(&self, url: &str) -> Result<Url> {
        if url.starts_with("/") {
            anyhow::bail!(
                "relative url: {} should not start with a slash",
                url
            );
        }

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

    pub async fn get_json<T: DeserializeOwned>(&self, url: &str) -> Result<T> {
        let res = self
            .get(url)?
            .send()
            .await?
            .error_for_status()?
            .json::<T>()
            .await?;
        Ok(res)
    }

    pub async fn post_json<
        Payload: Serialize + ?Sized,
        Res: DeserializeOwned,
    >(
        &self,
        url: &str,
        payload: &Payload,
    ) -> Result<Res> {
        let res = self
            .post(url)?
            .json(payload)
            .send()
            .await?
            .error_for_status()?
            .json()
            .await?;
        Ok(res)
    }

    /// given an [`anyhow::Error`], if its a 404 error from [`reqwest::Error`]
    /// return [`None`], otherwise return the error
    pub fn handle_404<T>(e: anyhow::Error) -> Result<Option<T>> {
        // NOTE: would this generate a new def for each T this is called on even
        // if T is not used in this?
        match e.downcast_ref::<reqwest::Error>() {
            Some(http_error) => {
                if http_error.status() == Some(reqwest::StatusCode::NOT_FOUND) {
                    Ok(None)
                } else {
                    Err(e)
                }
            }
            None => Err(e),
        }
    }
}
