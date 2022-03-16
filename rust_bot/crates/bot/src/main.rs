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

/// Wrapper around my discord id
pub struct OwnerHolder;

impl serenity::prelude::TypeMapKey for OwnerHolder {
    type Value = u64;
}

#[tokio::main]
async fn main() {
    env_logger::init();
    let framework = create_framework();

    let token = env::var("DISCORD_ID").expect("DISCORD_ID not set");
    let base_url = env::var("BACKEND_URL").expect("BACKEND_URL not set");
    let api_key = env::var("BOT_API_TOKEN").expect("BOT_API_TOKEN not set");
    let owner_id: u64 = env::var("BOT_ADMIN")
        .expect("BOT_ADMIN not set")
        .parse()
        .expect("Bot admin var not an usize");

    let mut client = Client::builder(token.trim())
        .event_handler(Handler)
        .framework(framework)
        .type_map_insert::<ThiccHolder>(ThiccClient::new(base_url, &api_key))
        .type_map_insert::<OwnerHolder>(owner_id)
        .await
        .expect("Error creating client");

    info!("Starting Bot");
    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        error!("An error occurred while running the client: {:?}", why);
    }
}
