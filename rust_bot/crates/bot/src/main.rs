#[macro_use]
extern crate log;
mod commands;
mod framework;
mod handler;
mod utils;

use client::ThiccClient;
use handler::Handler;
use serenity::client::Client;

use std::env;

use crate::framework::create_framework;

/// Wrapper around ThiccClient to be re used in each command/handler
pub struct ThiccHolder;

impl serenity::prelude::TypeMapKey for ThiccHolder {
    type Value = ThiccClient;
}

#[tokio::main]
async fn main() {
    env_logger::init();
    let framework = create_framework();

    let base_url = "http://localhost:5000/api/"; // TODO: read from env var
    let api_key = env::var("BOT_API_TOKEN").expect("BOT_API_TOKEN");

    // Login with a bot token from the environment
    let token = env::var("DISCORD_ID").expect("DISCORD_ID");
    let mut client = Client::builder(token)
        .event_handler(Handler)
        .framework(framework)
        .type_map_insert::<ThiccHolder>(ThiccClient::new(base_url, &api_key))
        .await
        .expect("Error creating client");

    info!("Starting Bot");
    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        error!("An error occurred while running the client: {:?}", why);
    }
}
