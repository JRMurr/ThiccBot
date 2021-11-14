use anyhow::Context;
use error::ThiccError;
use reqwest::{
    header::{HeaderMap, HeaderValue, AUTHORIZATION},
    Client, RequestBuilder, Url,
};
use serde::{de::DeserializeOwned, Serialize};
use std::collections::HashMap;

pub mod error;
pub mod guilds;
pub mod key_words;

type ErrorMap = HashMap<reqwest::StatusCode, ThiccError>;

/// Wrapper around [`Client`] to support a `base_url`
#[derive(Debug, Clone)]
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

    fn join_with_base(&self, url: &str) -> anyhow::Result<Url> {
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

    pub fn post(&self, url: &str) -> anyhow::Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.post(url))
    }

    pub fn get(&self, url: &str) -> anyhow::Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.get(url))
    }

    pub fn delete(&self, url: &str) -> anyhow::Result<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.delete(url))
    }

    pub async fn get_json<T: DeserializeOwned>(
        &self,
        url: &str,
    ) -> anyhow::Result<T> {
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
    ) -> anyhow::Result<Res> {
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

    /// given an [`anyhow::Result`], if its a 404 error from [`reqwest::Error`]
    /// return [`None`], otherwise return the passed result
    pub fn swallow_404<T>(
        result: anyhow::Result<T>,
    ) -> anyhow::Result<Option<T>> {
        match result {
            Ok(value) => Ok(Some(value)),
            Err(e) => match e.downcast_ref::<reqwest::Error>() {
                Some(http_error)
                    if http_error.status()
                        == Some(reqwest::StatusCode::NOT_FOUND) =>
                {
                    Ok(None)
                }
                _ => Err(e),
            },
        }
    }

    pub fn handle_status<T>(
        result: anyhow::Result<T>,
        mut statuses: ErrorMap,
    ) -> anyhow::Result<T> {
        match result {
            Ok(value) => Ok(value),
            Err(e) => match e.downcast_ref::<reqwest::Error>() {
                Some(http_error) => match http_error.status() {
                    Some(status) => match statuses.remove(&status) {
                        Some(err) => Err(err.into()),
                        None => Err(e),
                    },
                    _ => Err(e),
                },
                _ => Err(e),
            },
        }
    }
}
