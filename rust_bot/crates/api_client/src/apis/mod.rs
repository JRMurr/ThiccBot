use hyper;
use serde;
use serde_json;

#[derive(Debug)]
pub enum Error<T> {
    Hyper(hyper::Error),
    Serde(serde_json::Error),
    ApiError(ApiError<T>),
}

#[derive(Debug)]
pub struct ApiError<T> {
    pub code: hyper::StatusCode,
    pub content: Option<T>,
}

impl<'de, T> From<(hyper::StatusCode, &'de [u8])> for Error<T> 
    where T: serde::Deserialize<'de> {
    fn from(e: (hyper::StatusCode, &'de [u8])) -> Self {
        if e.1.len() == 0 {
            return Error::ApiError(ApiError{
                code: e.0,
                content: None,
            });
        }
        match serde_json::from_slice::<T>(e.1) {
            Ok(t) => Error::ApiError(ApiError{
                code: e.0,
                content: Some(t),
            }),
            Err(e) => {
                Error::from(e)
            }
        }
    }
}

impl<T> From<hyper::Error> for Error<T> {
    fn from(e: hyper::Error) -> Self {
        return Error::Hyper(e)
    }
}

impl<T> From<serde_json::Error> for Error<T> {
    fn from(e: serde_json::Error) -> Self {
        return Error::Serde(e)
    }
}

use super::models::*;

mod apialbums_api;
pub use self::apialbums_api::{ ApialbumsApi, ApialbumsApiClient };
mod apialias_api;
pub use self::apialias_api::{ ApialiasApi, ApialiasApiClient };
mod apicounter_api;
pub use self::apicounter_api::{ ApicounterApi, ApicounterApiClient };
mod apidiscord_api;
pub use self::apidiscord_api::{ ApidiscordApi, ApidiscordApiClient };
mod apidiscordroles_api;
pub use self::apidiscordroles_api::{ ApidiscordrolesApi, ApidiscordrolesApiClient };
mod apikey_words_api;
pub use self::apikey_words_api::{ ApikeyWordsApi, ApikeyWordsApiClient };
mod apilast_fm_api;
pub use self::apilast_fm_api::{ ApilastFMApi, ApilastFMApiClient };
mod apiquotes_api;
pub use self::apiquotes_api::{ ApiquotesApi, ApiquotesApiClient };
mod apistandings_api;
pub use self::apistandings_api::{ ApistandingsApi, ApistandingsApiClient };

pub mod configuration;
pub mod client;
