#[macro_use]
extern crate log;
mod commands;
mod handler;

use client::ThiccClient;
use commands::key_words::KEYWORDS_GROUP;
use handler::Handler;
use serenity::{
    client::{Client, Context},
    framework::standard::{
        macros::{command, group, help},
        Args, CommandGroup, CommandResult, HelpOptions, StandardFramework,
    },
    model::channel::Message,
};

use std::{collections::HashSet, env};

#[help]
async fn my_help(
    context: &Context,
    msg: &Message,
    args: Args,
    help_options: &'static HelpOptions,
    groups: &[&'static CommandGroup],
    owners: HashSet<serenity::model::id::UserId>,
) -> CommandResult {
    let _ = serenity::framework::standard::help_commands::with_embeds(
        context,
        msg,
        args,
        help_options,
        groups,
        owners,
    )
    .await;
    Ok(())
}

#[group]
#[commands(ping)]
struct General;

#[tokio::main]
async fn main() {
    env_logger::init();

    // TODO: look into https://docs.rs/serenity/0.10.9/serenity/framework/standard/struct.Configuration.html#method.dynamic_prefix
    // to be able to set the prefix per server
    // TODO: add error handler
    let framework = StandardFramework::new()
        .configure(|c| c.prefix("?")) // set the bot's prefix to "?"
        .help(&MY_HELP)
        .group(&GENERAL_GROUP)
        .group(&KEYWORDS_GROUP);

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

    info!("Starting Bot");
    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        error!("An error occurred while running the client: {:?}", why);
    }
}

#[command]
async fn ping(ctx: &Context, msg: &Message) -> CommandResult {
    msg.reply(ctx, "Pong!").await?;

    Ok(())
}
