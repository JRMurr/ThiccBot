use std::str::FromStr;
use strum::{Display, EnumVariantNames, VariantNames};

use crate::{error::ThiccError, ThiccClient, ThiccResult};

use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Debug, Serialize, Deserialize, Clone)]
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

    pub command_prefixes: Option<Vec<String>>,
    pub message_prefixes: Option<Vec<String>>,
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

#[derive(Debug, Display, EnumVariantNames, PartialEq)]
pub enum PrefixType {
    #[strum(to_string = "message prefix")]
    Message,
    #[strum(to_string = "command prefix")]
    Command,
}

impl FromStr for PrefixType {
    type Err = ThiccError;
    fn from_str(s: &str) -> Result<PrefixType, ThiccError> {
        match s.trim() {
            "message" => Ok(PrefixType::Message),
            "command" => Ok(PrefixType::Command),
            _ => Err(ThiccError::ParseError {
                allowed: PrefixType::VARIANTS,
                got: s.to_string(),
            }),
        }
    }
}

// TODO: add my guild stuff to the cache
impl GuildManager<'_> {
    async fn swallow_and_cache(
        &self,
        guild_id: u64,
        res: ThiccResult<DiscordGuild>,
    ) -> ThiccResult<Option<DiscordGuild>> {
        let res = ThiccClient::swallow_404(res);

        if let Ok(Some(ref guild)) = res {
            self.client
                .guild_cache
                .insert(guild_id, guild.clone())
                .await;
        }
        res
    }

    pub async fn get(
        &self,
        guild_id: u64,
    ) -> ThiccResult<Option<DiscordGuild>> {
        if let Some(guild) = self.client.guild_cache.get(&guild_id) {
            return Ok(Some(guild));
        }
        let res: ThiccResult<DiscordGuild> = self
            .client
            .get_json(format!("{}/{}", self.route, guild_id))
            .await;
        self.swallow_and_cache(guild_id, res).await
    }

    pub async fn set_bot_admin(
        &self,
        guild_id: u64,
        role_id: u64,
    ) -> ThiccResult<Option<DiscordGuild>> {
        let res: ThiccResult<DiscordGuild> = self
            .client
            .put_json(
                format!("{}/{}", self.route, guild_id),
                &json!({ "admin_role": role_id }),
            )
            .await;
        self.swallow_and_cache(guild_id, res).await
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
        let res: ThiccResult<DiscordGuild> =
            self.client.post_json(&self.route, &payload).await;
        let mapped_res = ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::BAD_REQUEST {
                Some(ThiccError::ResourceAlreadyExist {
                    name: payload.name.clone(),
                    resource_type: "Guild".to_string(),
                })
            } else {
                None
            }
        });

        if let Ok(ref guild) = mapped_res {
            self.client
                .guild_cache
                .insert(guild_id, guild.clone())
                .await;
        }
        mapped_res
    }

    pub async fn create_prefix(
        &self,
        guild_id: u64,
        prefix_type: &PrefixType,
        prefix: &str,
    ) -> ThiccResult<Option<DiscordGuild>> {
        let res: ThiccResult<DiscordGuild> = self
            .client
            .put_json(
                format!("{}/{}", self.route, guild_id),
                &json!({ prefix_type.to_string(): prefix }),
            )
            .await;
        self.swallow_and_cache(guild_id, res).await
    }
}
