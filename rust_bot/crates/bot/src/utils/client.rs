use client::ThiccClient;
use serenity::{client::Context, model::channel::Message};

use crate::ThiccHolder;

use super::BotUtils;

impl BotUtils {
    pub async fn get_thicc_client(
        ctx: &Context,
    ) -> anyhow::Result<ThiccClient> {
        let data = ctx.data.read().await;
        match data.get::<ThiccHolder>().cloned() {
            Some(thicc_client) => Ok(thicc_client),
            None => anyhow::bail!("Error getting thicc client"),
        }
    }

    pub fn get_guild_id(msg: &Message) -> anyhow::Result<u64> {
        match msg.guild_id {
            Some(id) => Ok(id.0),
            None => anyhow::bail!("Error getting guild id"),
        }
    }

    /// Get the guild id and thicc client from the msg and context
    pub async fn get_info(
        ctx: &Context,
        msg: &Message,
    ) -> anyhow::Result<(ThiccClient, u64)> {
        let thicc_client = BotUtils::get_thicc_client(ctx).await?;
        let guild_id = BotUtils::get_guild_id(msg)?;
        Ok((thicc_client, guild_id))
    }
}
