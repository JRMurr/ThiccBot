use client::ThiccClient;
use serenity::async_trait;
use serenity::client::{Client, Context, EventHandler};
use serenity::framework::standard::{
    macros::{command, group},
    CommandResult, StandardFramework,
};
use serenity::model::channel::Message;

// use client::models::key_word::KeyWord;
use std::env;

#[group]
#[commands(ping)]
struct General;

struct Handler {
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
}

#[tokio::main]
async fn main() {
    let framework = StandardFramework::new()
        .configure(|c| c.prefix("?")) // set the bot's prefix to "?"
        .group(&GENERAL_GROUP);

    let base_url = "http://localhost:5000"; // TODO: read from env var
    let api_key = env::var("BOT_API_TOKEN").expect("BOT_API_TOKEN");
    let thicc_client = ThiccClient::new(base_url, &api_key);

    let handler = Handler {
        client: thicc_client,
    };

    // Login with a bot token from the environment
    let token = env::var("DISCORD_ID").expect("DISCORD_ID");
    let mut client = Client::builder(token)
        .event_handler(handler)
        .framework(framework)
        .await
        .expect("Error creating client");

    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        println!("An error occurred while running the client: {:?}", why);
    }
}

#[command]
async fn ping(ctx: &Context, msg: &Message) -> CommandResult {
    msg.reply(ctx, "Pong!").await?;

    Ok(())
}
