use crate::utils::{
    checks::BOT_ADMIN_CHECK, paginate::PageDisplay, ArgParser, BotUtils,
};
use client::quotes::{Quote, QuoteCreate};
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

#[group]
#[prefixes(quotes, quote)]
#[commands(create, list, get, search, delete)]
#[default_command(get)] // TODO: its a little weird, when u miss type a sub command it runs get
#[summary = "Commands for creating and managing quotes"]
#[only_in(guilds)]
pub struct Quotes; // TODO: add bot admin checks

impl PageDisplay for Quote {
    fn page_display(&self) -> String {
        format!("{}: {}", self.id, self)
    }
}

#[command]
#[aliases("set", "make", "add", "save")]
#[checks(BOT_ADMIN)]
#[min_args(2)]
async fn create(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let quote: QuoteCreate = ArgParser::key_value_pair(args)?.into();

    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;

    let res = client.quotes(guild_id).create(&quote).await?;

    msg.reply(ctx, format!("Created quote: {}", res)).await?;

    Ok(())
}

#[command]
#[num_args(0)]
async fn list(ctx: &Context, msg: &Message) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let res = client.quotes(guild_id).list().await?;

    BotUtils::run_paged_menu(ctx, msg, res).await?;

    Ok(())
}

#[command]
#[num_args(1)]
async fn search(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let search_text = args.single_quoted::<String>()?;

    let res = client.quotes(guild_id).search(search_text).await?;
    let str =
        res.map_or("No quote found".to_string(), |quote| format!("{}", quote));

    msg.reply(ctx, str).await?;
    Ok(())
}

#[command]
#[num_args(0)]
async fn get(ctx: &Context, msg: &Message) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let res = client.quotes(guild_id).get_random().await?;
    let str =
        res.map_or("No quote found".to_string(), |quote| format!("{}", quote));

    msg.reply(ctx, str).await?;
    Ok(())
}

#[command]
#[checks(BOT_ADMIN)]
#[num_args(1)]
async fn delete(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let quote_id = args.single_quoted::<usize>()?;
    client.quotes(guild_id).delete(quote_id).await?;

    msg.reply(ctx, format!("Deleted quote: {}", quote_id))
        .await?;

    Ok(())
}
