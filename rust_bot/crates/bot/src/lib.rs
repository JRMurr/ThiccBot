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

pub async fn build_bot() -> Client {
    let owner_id = env::var("BOT_ADMIN")
        .expect("BOT_ADMIN not set")
        .trim()
        .parse()
        .expect("Bot admin var not an usize");

    let bot_user_id = env::var("BOT_USER_ID")
        .map(|id| id.trim().parse().expect("BOT_USER_ID is not valid"))
        .ok();
    let framework = create_framework(owner_id, bot_user_id);

    let token = env::var("DISCORD_ID").expect("DISCORD_ID not set");
    let base_url = env::var("BACKEND_URL").expect("BACKEND_URL not set");
    let api_key = env::var("BOT_API_TOKEN").expect("BOT_API_TOKEN not set");

    Client::builder(token.trim())
        .event_handler(Handler)
        .framework(framework)
        .type_map_insert::<ThiccHolder>(ThiccClient::new(base_url, &api_key))
        .await
        .expect("Error creating client")
}
