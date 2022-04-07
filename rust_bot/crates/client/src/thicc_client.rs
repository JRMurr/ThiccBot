use std::{fmt, time::Duration};

use crate::{
    error::{ClientErrors, ThiccError},
    guilds,
};
use anyhow::Context;
use bytes::Bytes;
use moka::future::Cache;
use reqwest::{
    header::{HeaderMap, HeaderValue, AUTHORIZATION},
    Client, IntoUrl, RequestBuilder, Url,
};
use serde::{de::DeserializeOwned, Serialize};

pub type ThiccResult<T> = std::result::Result<T, ClientErrors>;

/// Wrapper around [`Client`] to support a `base_url`
#[allow(dead_code)] // clone is used in client
#[derive(Clone)]
pub struct ThiccClient {
    client: Client,
    base_url: Url,
    // TODO: maybe generalize this for all resources, could be useful for
    // aliases and keywords
    pub(crate) guild_cache: Cache<u64, guilds::DiscordGuild>,

    general_cache: Cache<String, Bytes>,
}

impl fmt::Debug for ThiccClient {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.debug_struct("ThiccClient")
            .field("client", &self.client)
            .field("base_url", &self.base_url)
            .finish_non_exhaustive()
    }
}

impl ThiccClient {
    /// Makes a new [`ThiccClient`] with the provided `base_url` and `api_key`
    pub fn new<U: IntoUrl>(base_url: U, api_key: &str) -> ThiccClient {
        let base_url: Url =
            base_url.into_url().expect("Error parsing base_url");

        let mut headers = HeaderMap::new();
        let mut auth_value =
            HeaderValue::from_str(api_key).expect("Error parsing api_key");
        auth_value.set_sensitive(true);
        headers.insert(AUTHORIZATION, auth_value);

        let client = Client::builder()
            .default_headers(headers)
            .build()
            .expect("Error building client");

        let guild_cache = Cache::builder()
            .max_capacity(100)
            .time_to_live(Duration::from_secs(10)) // all the calls should update the cache as needed. If other bots
            // frontends are added maybe lower this
            .build();

        let general_cache = Cache::builder()
            .max_capacity(10_000)
            .time_to_live(Duration::from_secs(10))
            .build();

        ThiccClient {
            client,
            base_url,
            guild_cache,
            general_cache,
        }
    }

    fn get_from_cache<U: IntoUrl, T: DeserializeOwned>(
        &self,
        url: &U,
    ) -> Option<T> {
        let key = url.as_str().to_string();
        if let Some(bytes) = self.general_cache.get(&key) {
            serde_json::from_slice(&bytes).ok()
        } else {
            None
        }
    }

    async fn cache_bytes<U: IntoUrl, Res: DeserializeOwned>(
        &self,
        url: &U,
        bytes: &Bytes,
    ) -> ThiccResult<Res> {
        let key = url.as_str().to_string();
        self.general_cache.insert(key, bytes.clone()).await;
        Ok(serde_json::from_slice(bytes)?)
    }

    fn join_with_base<U: IntoUrl>(&self, url: &U) -> ThiccResult<Url> {
        let url = url.as_str();
        if url.starts_with('/') {
            return Err(ClientErrors::InvalidRelativeUrl(url.to_string()));
        }

        let url = self
            .base_url
            .join(url)
            .with_context(|| format!("Failed parsing relative url {}", url))?;
        Ok(url)
    }

    pub fn post<U: IntoUrl>(&self, url: &U) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.post(url))
    }

    pub fn get<U: IntoUrl>(&self, url: &U) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.get(url))
    }

    pub fn delete<U: IntoUrl>(&self, url: &U) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.delete(url))
    }

    pub fn put<U: IntoUrl>(&self, url: &U) -> ThiccResult<RequestBuilder> {
        let url = self.join_with_base(url)?;
        Ok(self.client.put(url))
    }

    pub async fn delete_helper<U: IntoUrl>(&self, url: U) -> ThiccResult<()> {
        let _ = self.delete(&url)?.send().await?.error_for_status();
        Ok(())
    }

    /// Gets a resource as the url, will lookup in cache. If not found will
    /// cache the result
    pub async fn get_json<T: DeserializeOwned, U: IntoUrl>(
        &self,
        url: U,
    ) -> ThiccResult<T> {
        if let Some(res) = self.get_from_cache(&url) {
            return Ok(res);
        }
        let res = self
            .get(&url)?
            .send()
            .await?
            .error_for_status()?
            .bytes()
            .await?;
        self.cache_bytes(&url, &res).await
    }

    pub async fn get_bytes<U: IntoUrl>(&self, url: U) -> ThiccResult<Bytes> {
        let res = self
            .get(&url)?
            .send()
            .await?
            .error_for_status()?
            .bytes()
            .await?;
        Ok(res)
    }

    /// Gets a resource as the url, will cache the result
    pub async fn post_json<
        Payload: Serialize + ?Sized,
        Res: DeserializeOwned,
        U: IntoUrl,
    >(
        &self,
        url: U,
        payload: &Payload,
    ) -> ThiccResult<Res> {
        let res = self
            .post(&url)?
            .json(payload)
            .send()
            .await?
            .error_for_status()?
            .bytes()
            .await?;
        self.cache_bytes(&url, &res).await
    }

    /// Gets a resource as the url, will cache the result
    pub async fn put_json<
        Payload: Serialize + ?Sized,
        Res: DeserializeOwned,
        U: IntoUrl,
    >(
        &self,
        url: U,
        payload: &Payload,
    ) -> ThiccResult<Res> {
        let res = self
            .put(&url)?
            .json(payload)
            .send()
            .await?
            .error_for_status()?
            .bytes()
            .await?;
        self.cache_bytes(&url, &res).await
    }

    /// given an [`ThiccResult`], if its a 404 error from [`reqwest::Error`]
    /// return [`None`], otherwise return the passed result
    pub fn swallow_404<T>(result: ThiccResult<T>) -> ThiccResult<Option<T>> {
        match result {
            Ok(value) => Ok(Some(value)),
            Err(ClientErrors::Reqwest(req_error))
                if req_error.status()
                    == Some(reqwest::StatusCode::NOT_FOUND) =>
            {
                Ok(None)
            }
            Err(e) => Err(e),
        }
    }

    pub fn handle_status<
        T,
        F: FnOnce(reqwest::StatusCode) -> Option<ThiccError>,
    >(
        result: ThiccResult<T>,
        err_map: F,
    ) -> ThiccResult<T> {
        match result {
            Ok(value) => Ok(value),
            Err(ClientErrors::Reqwest(req_error)) => match req_error.status() {
                Some(status) => match err_map(status) {
                    Some(err) => Err(err.into()),
                    None => Err(req_error.into()),
                },
                _ => Err(req_error.into()),
            },
            Err(e) => Err(e),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use httptest::{
        matchers::*,
        responders::{self, *},
        Expectation, ExpectationBuilder, ServerHandle, ServerPool,
    };

    use rstest::*;
    use serde::Deserialize;

    static SERVER_POOL: ServerPool = ServerPool::new(10);
    static API_KEY: &str = "apiKey";

    #[fixture]
    pub fn server() -> ServerHandle<'static> {
        let _ = pretty_env_logger::try_init();
        SERVER_POOL.get_server()
    }

    fn get_client(server: &ServerHandle<'static>) -> ThiccClient {
        let url = server.url("").to_string();
        ThiccClient::new(url, API_KEY)
    }

    fn get_expected_path(
        method: &'static str,
        path: &'static str,
    ) -> ExpectationBuilder {
        Expectation::matching(all_of![
            request::method_path(method, path),
            request::headers(contains(("authorization", API_KEY)))
        ])
    }

    #[rstest]
    #[tokio::test]
    async fn test_get_add_base(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("GET", "/foo").respond_with(status_code(200)),
        );

        let resp = client.get(&"foo")?.send().await?;

        assert!(resp.status().is_success());

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_post_add_base(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("POST", "/foo").respond_with(status_code(200)),
        );

        let resp = client.post(&"foo")?.send().await?;

        assert!(resp.status().is_success());

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_delete_add_base(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("DELETE", "/foo").respond_with(status_code(200)),
        );

        let resp = client.delete(&"foo")?.send().await?;

        assert!(resp.status().is_success());

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_put_add_base(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("PUT", "/foo").respond_with(status_code(200)),
        );

        let resp = client.put(&"foo")?.send().await?;

        assert!(resp.status().is_success());

        Ok(())
    }

    #[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
    struct TestStruct {
        pub key: usize,
    }

    #[rstest]
    #[tokio::test]
    async fn test_get_json(server: ServerHandle<'static>) -> ThiccResult<()> {
        let client = get_client(&server);

        let body = TestStruct { key: 10 };

        server.expect(
            get_expected_path("GET", "/foo")
                .respond_with(responders::json_encoded(&body)),
        );

        let resp: TestStruct = client.get_json("foo").await?;

        assert_eq!(resp, body);

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_get_json_reqwest_error(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("GET", "/foo").respond_with(status_code(404)),
        );

        let resp: ThiccResult<usize> = client.get_json("foo").await;

        assert_matches!(resp, Err(ClientErrors::Reqwest(_)));

        assert_matches!(ThiccClient::swallow_404(resp), Ok(None));

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_handle_status(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        server.expect(
            get_expected_path("GET", "/foo").respond_with(status_code(404)),
        );

        let resp: ThiccResult<usize> = client.get_json("foo").await;

        assert_matches!(resp, Err(ClientErrors::Reqwest(_)));

        let new_error = ThiccError::ResourceAlreadyExist {
            name: "a name".to_string(),
            resource_type: "a resource".to_string(),
        };

        let new_resp = ThiccClient::handle_status(resp, |status| {
            if status == reqwest::StatusCode::NOT_FOUND {
                Some(new_error)
            } else {
                None
            }
        });

        assert_matches!(
            new_resp,
            Err(ClientErrors::Thicc(ThiccError::ResourceAlreadyExist {
                resource_type: _,
                name: _
            }))
        );

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_post_json(server: ServerHandle<'static>) -> ThiccResult<()> {
        let client = get_client(&server);

        let body = TestStruct { key: 10 };

        server.expect(
            get_expected_path("POST", "/foo")
                .respond_with(responders::json_encoded(&body)),
        );

        let resp: TestStruct = client.post_json("foo", &body).await?;

        assert_eq!(resp, body);

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_post_json_reqwest_error(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        let body = TestStruct { key: 10 };

        server.expect(
            get_expected_path("POST", "/foo").respond_with(status_code(404)),
        );

        let resp: ThiccResult<usize> = client.post_json("foo", &body).await;

        assert_matches!(resp, Err(ClientErrors::Reqwest(_)));

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_put_json(server: ServerHandle<'static>) -> ThiccResult<()> {
        let client = get_client(&server);

        let body = TestStruct { key: 10 };

        server.expect(
            get_expected_path("PUT", "/foo")
                .respond_with(responders::json_encoded(&body)),
        );

        let resp: TestStruct = client.put_json("foo", &body).await?;

        assert_eq!(resp, body);

        Ok(())
    }

    #[rstest]
    #[tokio::test]
    async fn test_put_json_reqwest_error(
        server: ServerHandle<'static>,
    ) -> ThiccResult<()> {
        let client = get_client(&server);

        let body = TestStruct { key: 10 };

        server.expect(
            get_expected_path("PUT", "/foo").respond_with(status_code(404)),
        );

        let resp: ThiccResult<usize> = client.put_json("foo", &body).await;

        assert_matches!(resp, Err(ClientErrors::Reqwest(_)));

        Ok(())
    }
}
