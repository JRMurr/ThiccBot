use anyhow::Result;
use client::ThiccClient;
use serenity::{
    async_trait,
    client::{Context, EventHandler},
    model::{channel::Message, guild::Guild},
};

pub struct Handler {
    client: ThiccClient,
}

impl Handler {
    pub fn new(client: ThiccClient) -> Handler {
        Self { client }
    }
}

impl Handler {
    async fn handle_key_words(
        &self,
        _context: &Context,
        msg: &Message,
    ) -> Result<()> {
        match msg.guild_id {
            Some(id) => {
                let key_words =
                    self.client.key_words().get(id.0, &msg.content).await?;
                trace!("key_words: {:?}", key_words);
                Ok(())
            }
            None => Ok(()),
        }
    }
}

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, context: Context, msg: Message) {
        if let Err(why) = self.handle_key_words(&context, &msg).await {
            error!("error handling key_words: {:?}", why);
        }
    }

    async fn guild_create(
        &self,
        _context: Context,
        guild: Guild,
        _is_new: bool,
    ) {
        let id = guild.id.0;
        match self.client.get_guild(id).await {
            Ok(None) => {
                // create guild in backend
                let res = self.client.create_guild(id, &guild.name).await;
                if let Err(why) = res {
                    error!("error making guild: {:?}", why);
                }
            }
            Err(why) => {
                error!("error getting guild: {:?}", why);
            }
            _ => return, // exists in backend already don't care
        }
    }
}
