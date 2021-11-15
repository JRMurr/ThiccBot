use std::collections::HashMap;

use crate::{error::ThiccError, ErrorMap, ThiccClient, ThiccResult};
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

    command_prefixes: Option<Vec<String>>,
    message_prefixes: Option<Vec<String>>,
}

#[derive(Debug, Serialize, Deserialize)]
struct DiscordGuildCreate {
    /// the name of the server/guild
    name: String,
    /// the guild id
    id: u64,
}

pub struct GuildManager<'a> {
    client: &'a ThiccClient,
    route: String,
}

const GUILD_ROUTE: &str = "discord";

impl ThiccClient {
    pub fn guilds(&self) -> GuildManager {
        GuildManager {
            client: &self,
            route: GUILD_ROUTE.to_string(),
        }
    }
}

impl GuildManager<'_> {
    pub async fn get(
        &self,
        guild_id: u64,
    ) -> ThiccResult<Option<DiscordGuild>> {
        let res = self
            .client
            .get_json::<DiscordGuild>(&format!("{}/{}", self.route, guild_id))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn create(
        &self,
        guild_id: u64,
        name: &str,
    ) -> ThiccResult<DiscordGuild> {
        let payload = DiscordGuildCreate {
            id: guild_id,
            name: name.to_string(),
        };
        let errors: ErrorMap = HashMap::from([(
            StatusCode::BAD_REQUEST,
            ThiccError::ResourceAlreadyExist {
                name: payload.name.clone(),
                resource_type: "Guild".to_string(),
            },
        )]);
        let res = self.client.post_json(&self.route, &payload).await;
        ThiccClient::handle_status(res, errors)
    }
}
