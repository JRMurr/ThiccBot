#[macro_use]
extern crate log;
mod commands;
mod framework;
mod handler;

use client::ThiccClient;
use handler::Handler;
use serenity::client::{Client, Context};

use std::env;

use crate::framework::create_framework;

/// Wrapper around ThiccClient to be re used in each command/handler
struct ClientHolder;

impl serenity::prelude::TypeMapKey for ClientHolder {
    type Value = ThiccClient;
}

// TODO: should this be a func in ThiccClient? It would be nice but adding
// serenity as a dep would be annoying
pub async fn get_thicc_client(ctx: &Context) -> anyhow::Result<ThiccClient> {
    let data = ctx.data.read().await;
    match data.get::<ClientHolder>().cloned() {
        Some(thicc_client) => Ok(thicc_client),
        None => anyhow::bail!("Error getting thicc client"),
    }
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
        .type_map_insert::<ClientHolder>(ThiccClient::new(base_url, &api_key))
        .await
        .expect("Error creating client");

    info!("Starting Bot");
    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        error!("An error occurred while running the client: {:?}", why);
    }
}
