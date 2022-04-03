use anyhow::Result;
use serenity::{
    async_trait,
    client::{Context, EventHandler},
    model::guild::Guild,
};

use crate::utils::BotUtils;

pub struct Handler;

impl Handler {
    async fn handle_guild_create(
        &self,
        ctx: &Context,
        guild: &Guild,
    ) -> Result<()> {
        let id = guild.id.0;
        let client = BotUtils::get_thicc_client(ctx).await?;
        let existing_guild = client.guilds().get(id).await?;
        if existing_guild.is_none() {
            client.guilds().create(id, &guild.name).await?;
        }
        Ok(())
    }
}

#[async_trait]
impl EventHandler for Handler {
    async fn guild_create(&self, ctx: Context, guild: Guild, _is_new: bool) {
        if let Err(why) = self.handle_guild_create(&ctx, &guild).await {
            error!("error handling guild_create: {:?}", why);
        }
    }
}
