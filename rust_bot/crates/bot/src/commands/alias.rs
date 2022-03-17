use crate::utils::{checks::BOT_ADMIN_CHECK, ArgParser, BotUtils};
use client::alias::Alias;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

#[group]
#[prefixes(alias)]
#[commands(create, list, delete)]
#[summary = "Commands for creating and managing key words"]
#[only_in(guilds)]
pub struct Aliases; // TODO: add bot admin checks

#[command]
#[aliases("set", "make", "add", "save")]
#[checks(BOT_ADMIN)]
#[min_args(2)]
async fn create(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
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
#[checks(BOT_ADMIN)]
#[num_args(1)]
async fn delete(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let name = args.single_quoted::<String>()?;
    client.alias(guild_id).delete(&name).await?;

    msg.reply(ctx, format!("Deleted alias: {}", name)).await?;

    Ok(())
}
