use crate::ThiccClient;
use anyhow::Result;
use reqwest::StatusCode;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct DiscordGuild {
    /// the name of the server/guild
    name: String,
    /// the guild id
    id: u64,
    /// The id of the guild in the backend
    server_group_id: u64,

    admin_role: Option<u64>,

    // TODO: check if these need to be options, the server might send an empty
    // array
    command_prefixes: Vec<String>,
    message_prefixes: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct DiscordGuildCreate {
    /// the name of the server/guild
    name: String,
    /// the guild id
    id: u64,
}

impl ThiccClient {
    pub async fn get_guild(
        &self,
        guild_id: u64,
    ) -> Result<Option<DiscordGuild>> {
        let res = self.get(&format!("/discord/{}", guild_id))?.send().await?;
        match res.error_for_status() {
            Ok(response) => Ok(Some(response.json::<DiscordGuild>().await?)),
            Err(e) => {
                if e.status() == Some(StatusCode::NOT_FOUND) {
                    Ok(None)
                } else {
                    Err(e.into())
                }
            }
        }
    }

    pub async fn create_guild(
        &self,
        guild_id: u64,
        name: &str,
    ) -> Result<DiscordGuild> {
        let payload = DiscordGuildCreate {
            id: guild_id,
            name: name.to_string(),
        };
        let res = self
            .post("/discord")?
            .json(&payload)
            .send()
            .await?
            .error_for_status()?
            .json()
            .await?;
        Ok(res)
    }
}
