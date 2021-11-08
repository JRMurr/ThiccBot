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

#[async_trait]
impl EventHandler for Handler {
    async fn message(&self, _context: Context, msg: Message) {
        match msg.guild_id {
            Some(id) => {
                let id = &id.0.to_string();
                match self.client.get_key_words(id, &msg.content).await {
                    Ok(key_words) => {
                        println!("key_words {:?}", key_words);
                    }
                    Err(why) => {
                        println!("error getting key_words: {:?}", why);
                    }
                }
            }
            None => return,
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
                    println!("error making guild: {:?}", why);
                }
            }
            Err(why) => {
                println!("error getting guild: {:?}", why);
            }
            _ => return, // exists in backend already don't care
        }
    }
}
