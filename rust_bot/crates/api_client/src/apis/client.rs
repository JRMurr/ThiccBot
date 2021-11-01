use std::rc::Rc;

use hyper;
use super::configuration::Configuration;

pub struct APIClient<C: hyper::client::Connect> {
  configuration: Rc<Configuration<C>>,
  apialbums_api: Box<::apis::ApialbumsApi>,
  apialias_api: Box<::apis::ApialiasApi>,
  apicounter_api: Box<::apis::ApicounterApi>,
  apidiscord_api: Box<::apis::ApidiscordApi>,
  apidiscordroles_api: Box<::apis::ApidiscordrolesApi>,
  apikey_words_api: Box<::apis::ApikeyWordsApi>,
  apilast_fm_api: Box<::apis::ApilastFMApi>,
  apiquotes_api: Box<::apis::ApiquotesApi>,
  apistandings_api: Box<::apis::ApistandingsApi>,
}

impl<C: hyper::client::Connect> APIClient<C> {
  pub fn new(configuration: Configuration<C>) -> APIClient<C> {
    let rc = Rc::new(configuration);

    APIClient {
      configuration: rc.clone(),
      apialbums_api: Box::new(::apis::ApialbumsApiClient::new(rc.clone())),
      apialias_api: Box::new(::apis::ApialiasApiClient::new(rc.clone())),
      apicounter_api: Box::new(::apis::ApicounterApiClient::new(rc.clone())),
      apidiscord_api: Box::new(::apis::ApidiscordApiClient::new(rc.clone())),
      apidiscordroles_api: Box::new(::apis::ApidiscordrolesApiClient::new(rc.clone())),
      apikey_words_api: Box::new(::apis::ApikeyWordsApiClient::new(rc.clone())),
      apilast_fm_api: Box::new(::apis::ApilastFMApiClient::new(rc.clone())),
      apiquotes_api: Box::new(::apis::ApiquotesApiClient::new(rc.clone())),
      apistandings_api: Box::new(::apis::ApistandingsApiClient::new(rc.clone())),
    }
  }

  pub fn apialbums_api(&self) -> &::apis::ApialbumsApi{
    self.apialbums_api.as_ref()
  }

  pub fn apialias_api(&self) -> &::apis::ApialiasApi{
    self.apialias_api.as_ref()
  }

  pub fn apicounter_api(&self) -> &::apis::ApicounterApi{
    self.apicounter_api.as_ref()
  }

  pub fn apidiscord_api(&self) -> &::apis::ApidiscordApi{
    self.apidiscord_api.as_ref()
  }

  pub fn apidiscordroles_api(&self) -> &::apis::ApidiscordrolesApi{
    self.apidiscordroles_api.as_ref()
  }

  pub fn apikey_words_api(&self) -> &::apis::ApikeyWordsApi{
    self.apikey_words_api.as_ref()
  }

  pub fn apilast_fm_api(&self) -> &::apis::ApilastFMApi{
    self.apilast_fm_api.as_ref()
  }

  pub fn apiquotes_api(&self) -> &::apis::ApiquotesApi{
    self.apiquotes_api.as_ref()
  }

  pub fn apistandings_api(&self) -> &::apis::ApistandingsApi{
    self.apistandings_api.as_ref()
  }


}
