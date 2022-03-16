use crate::{error::ThiccError, ThiccClient, ThiccResult};

use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Debug, Serialize, Deserialize)]
pub struct DiscordGuild {
    /// the name of the server/guild
    pub name: String,
    /// the guild id
    pub id: u64,
    /// the id of the guild in the backend
    pub server_group_id: u64,

    /// the role users must have to be allowed to create/update/delete
    /// resources in thicc bot this is based on the priority so if a user
    /// has a role above this role they are still an admin
    pub admin_role: Option<u64>,

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
            client: self,
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
            .get_json(format!("{}/{}", self.route, guild_id))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn set_bot_admin(
        &self,
        guild_id: u64,
        role_id: u64,
    ) -> ThiccResult<Option<DiscordGuild>> {
        let res = self
            .client
            .put_json(
                format!("{}/{}", self.route, guild_id),
                &json!({ "admin_role": role_id }),
            )
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
        let res = self.client.post_json(&self.route, &payload).await;
        ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::BAD_REQUEST {
                Some(ThiccError::ResourceAlreadyExist {
                    name: payload.name.clone(),
                    resource_type: "Guild".to_string(),
                })
            } else {
                None
            }
        })
    }
}
