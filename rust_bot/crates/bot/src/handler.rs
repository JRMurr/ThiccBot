use client::ThiccClient;
use serenity::{
    async_trait,
    client::{Client, Context, EventHandler},
    model::{channel::Message, guild::Guild},
};

pub struct Handler {
    client: ThiccClient,
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

    async fn guild_create(&self, _context: Context, guild: Guild) {}
}
