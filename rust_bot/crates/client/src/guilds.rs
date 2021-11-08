use crate::ThiccClient;
use anyhow::Result;
use reqwest::StatusCode;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct DiscordGuild {
    name: String,
    command_prefixes: Vec<String>,
    message_prefixes: Vec<String>,
    server_group_id: u64,
    id: u64,
    admin_role: u64,
}

impl ThiccClient {
    pub async fn get_guild(&self, guild_id: &str) -> Result<Option<DiscordGuild>> {
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

    // pub async fn create_guild(&self, guild)
}
