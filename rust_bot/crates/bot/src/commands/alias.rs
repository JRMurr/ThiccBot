use client::alias::Alias;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

use crate::utils::{ArgParser, BotUtils};

#[group]
#[prefixes(alias)]
#[commands(create, list)]
#[summary = "Commands for creating and managing key words"]
#[only_in(guilds)]
pub struct Aliases; // TODO: add bot admin checks

#[command]
#[aliases("set", "make", "add", "save")]
async fn create(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    // TODO: add some arg validation to reduce the risk of an error
    // https://docs.rs/serenity/0.10.9/serenity/framework/standard/macros/attr.command.html
    let alias: Alias = ArgParser::key_value_pair(args)?.into();

    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;

    let res = client.alias(guild_id).create(&alias).await?;

    msg.reply(ctx, format!("Created alias: {}", res.name))
        .await?;

    Ok(())
}

#[command]
async fn list(ctx: &Context, msg: &Message) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let res = client.alias(guild_id).list().await?;
    // // TODO: add emoji based pagination like old bot
    // // this lib might help https://github.com/AriusX7/serenity-utils
    // msg.reply(ctx, format!("{:?}", res)).await?;

    BotUtils::run_paged_menu(ctx, msg, res).await?;

    Ok(())
}

#[command]
async fn delete(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let name = args.single_quoted::<String>()?;
    client.alias(guild_id).delete(&name).await?;

    msg.reply(ctx, format!("Deleted alias: {}", name)).await?;

    Ok(())
}
