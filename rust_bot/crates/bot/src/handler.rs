use anyhow::Result;
use rand::seq::SliceRandom;
use serenity::{
    async_trait,
    client::{Context, EventHandler},
    model::{channel::Message, guild::Guild},
};

use crate::get_thicc_client;

pub struct Handler;

impl Handler {
    async fn handle_key_words(
        &self,
        ctx: &Context,
        msg: &Message,
    ) -> Result<()> {
        match msg.guild_id {
            Some(id) => {
                let client = get_thicc_client(ctx).await?;
                let key_word =
                    client.key_words().get(id.0, &msg.content).await?;
                match key_word {
                    Some(key_word) => {
                        let rand_response =
                            key_word.responses.choose(&mut rand::thread_rng());
                        match rand_response {
                            Some(response) => {
                                msg.channel_id.say(&ctx.http, response).await?;
                                Ok(())
                            }
                            None => anyhow::bail!(
                                "Key word does not have any responses"
                            ),
                        }
                    }
                    None => Ok(()),
                }
            }
            None => Ok(()),
        }
    }

    async fn handle_guild_create(
        &self,
        ctx: &Context,
        guild: &Guild,
    ) -> Result<()> {
        let id = guild.id.0;
        let client = get_thicc_client(&ctx).await?;
        let existing_guild = client.get_guild(id).await?;
        if existing_guild.is_none() {
            client.create_guild(id, &guild.name).await?;
        }
        Ok(())
    }
}

#[async_trait]
impl EventHandler for Handler {
    // TODO: might be able to do this in a .normal_message(normal_message)
    async fn message(&self, context: Context, msg: Message) {
        if let Err(why) = self.handle_key_words(&context, &msg).await {
            error!("error handling key_words: {:?}", why);
        }
    }

    async fn guild_create(&self, ctx: Context, guild: Guild, _is_new: bool) {
        if let Err(why) = self.handle_guild_create(&ctx, &guild).await {
            error!("error handling guild_create: {:?}", why);
        }
    }
}
