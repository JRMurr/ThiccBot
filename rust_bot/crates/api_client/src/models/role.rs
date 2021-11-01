/* 
 * API
 *
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 1.0
 * 
 * Generated by: https://github.com/swagger-api/swagger-codegen.git
 */


#[allow(unused_imports)]
use serde_json::Value;

#[derive(Debug, Serialize, Deserialize)]
pub struct Role {
  #[serde(rename = "role_id")]
  role_id: Option<i32>,
  #[serde(rename = "message_id")]
  message_id: Option<i32>,
  #[serde(rename = "channel_id")]
  channel_id: Option<i32>,
  #[serde(rename = "id")]
  id: Option<i32>
}

impl Role {
  pub fn new() -> Role {
    Role {
      role_id: None,
      message_id: None,
      channel_id: None,
      id: None
    }
  }

  pub fn set_role_id(&mut self, role_id: i32) {
    self.role_id = Some(role_id);
  }

  pub fn with_role_id(mut self, role_id: i32) -> Role {
    self.role_id = Some(role_id);
    self
  }

  pub fn role_id(&self) -> Option<&i32> {
    self.role_id.as_ref()
  }

  pub fn reset_role_id(&mut self) {
    self.role_id = None;
  }

  pub fn set_message_id(&mut self, message_id: i32) {
    self.message_id = Some(message_id);
  }

  pub fn with_message_id(mut self, message_id: i32) -> Role {
    self.message_id = Some(message_id);
    self
  }

  pub fn message_id(&self) -> Option<&i32> {
    self.message_id.as_ref()
  }

  pub fn reset_message_id(&mut self) {
    self.message_id = None;
  }

  pub fn set_channel_id(&mut self, channel_id: i32) {
    self.channel_id = Some(channel_id);
  }

  pub fn with_channel_id(mut self, channel_id: i32) -> Role {
    self.channel_id = Some(channel_id);
    self
  }

  pub fn channel_id(&self) -> Option<&i32> {
    self.channel_id.as_ref()
  }

  pub fn reset_channel_id(&mut self) {
    self.channel_id = None;
  }

  pub fn set_id(&mut self, id: i32) {
    self.id = Some(id);
  }

  pub fn with_id(mut self, id: i32) -> Role {
    self.id = Some(id);
    self
  }

  pub fn id(&self) -> Option<&i32> {
    self.id.as_ref()
  }

  pub fn reset_id(&mut self) {
    self.id = None;
  }

}



