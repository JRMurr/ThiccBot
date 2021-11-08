mod handler;

use crate::handler::Handler;
use client::ThiccClient;
use serenity::{
    client::{Client, Context},
    framework::standard::{
        macros::{command, group},
        CommandResult, StandardFramework,
    },
    model::channel::Message,
};

// use client::models::key_word::KeyWord;
use std::env;

#[group]
#[commands(ping)]
struct General;

#[tokio::main]
async fn main() {
    // TODO: look into https://docs.rs/serenity/0.10.9/serenity/framework/standard/struct.Configuration.html#method.dynamic_prefix
    // to be able to set the prefix per server
    let framework = StandardFramework::new()
        .configure(|c| c.prefix("?")) // set the bot's prefix to "?"
        .group(&GENERAL_GROUP);

    let base_url = "http://localhost:5000/api/"; // TODO: read from env var
    let api_key = env::var("BOT_API_TOKEN").expect("BOT_API_TOKEN");

    let handler = Handler::new(ThiccClient::new(base_url, &api_key));

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
