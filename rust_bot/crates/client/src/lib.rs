use anyhow::Context;
use error::{ClientErrors, ThiccError};
use reqwest::{
    header::{HeaderMap, HeaderValue, AUTHORIZATION},
    Client, RequestBuilder, Url,
};
use serde::{de::DeserializeOwned, Serialize};
use std::collections::HashMap;

pub mod alias;
pub mod error;
pub mod guilds;
pub mod key_words;

type ErrorMap = HashMap<reqwest::StatusCode, ThiccError>;

pub type ThiccResult<T> = std::result::Result<T, ClientErrors>;

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

    fn join_with_base(&self, url: &str) -> ThiccResult<Url> {
        if url.starts_with("/") {
            return Err(ClientErrors::InvalidRelativeUrl(url.to_string()));
        }

        let url = self
            .base_url
            .join(url)
            .with_context(|| format!("Failed parsing relative url {}", url))?;
        Ok(url)
    }

    pub fn post(&self, url: &str) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.post(url))
    }

    pub fn get(&self, url: &str) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.get(url))
    }

    pub fn delete(&self, url: &str) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.delete(url))
    }

    pub async fn delete_helper(&self, url: &str) -> ThiccResult<()> {
        let _ = self.delete(url)?.send().await?.error_for_status();
        Ok(())
    }

    pub async fn get_json<T: DeserializeOwned>(
        &self,
        url: &str,
    ) -> ThiccResult<T> {
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
    ) -> ThiccResult<Res> {
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

    /// given an [`ThiccResult`], if its a 404 error from [`reqwest::Error`]
    /// return [`None`], otherwise return the passed result
    pub fn swallow_404<T>(result: ThiccResult<T>) -> ThiccResult<Option<T>> {
        match result {
            Ok(value) => Ok(Some(value)),
            Err(ClientErrors::Reqwest(req_error)) if req_error.status() == Some(reqwest::StatusCode::NOT_FOUND) => {
                Ok(None)
            },
            Err(e) => Err(e)
            // Err(e) => match e.downcast_ref::<reqwest::Error>() {
            //     Some(http_error)
            //         if http_error.status()
            //             == Some(reqwest::StatusCode::NOT_FOUND) =>
            //     {
            //         Ok(None)
            //     }
            //     _ => Err(e),
            // },
        }
    }

    pub fn handle_status<T>(
        result: ThiccResult<T>,
        mut statuses: ErrorMap,
    ) -> ThiccResult<T> {
        match result {
            Ok(value) => Ok(value),
            Err(ClientErrors::Reqwest(req_error)) => match req_error.status() {
                Some(status) => match statuses.remove(&status) {
                    Some(err) => Err(err.into()),
                    None => Err(req_error.into()),
                },
                _ => Err(req_error.into()),
            },
            Err(e) => Err(e),
        }
    }
}
