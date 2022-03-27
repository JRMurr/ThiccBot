use crate::utils::{
    checks::BOT_ADMIN_CHECK, paginate::PageDisplay, ArgParser, BotUtils,
};
use client::key_words::KeyWord;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

#[group]
#[prefixes(keyWord, keyword, keyword, keyWords, key_word)]
#[commands(create, list, delete, update)]
#[summary = "Commands for creating and managing key words"]
#[only_in(guilds)]
pub struct KeyWords;

impl PageDisplay for KeyWord {
    fn page_display(&self) -> String {
        self.to_string()
    }
}

#[command]
#[aliases("set", "make", "add", "save")]
#[checks(BOT_ADMIN)]
#[min_args(2)]
async fn create(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    // TODO: this will only do one response, maybe allow multiple responses?
    let key_word: KeyWord = ArgParser::key_value_pair(args)?.into();

    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;

    let res = client.key_words(guild_id).create(&key_word).await?;

    msg.reply(ctx, format!("Created key word: {}", res.name))
        .await?;

    Ok(())
}

#[command]
#[aliases("update", "change")]
#[checks(BOT_ADMIN)]
#[min_args(2)]
async fn update(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let key_word: KeyWord = ArgParser::key_value_pair(args)?.into();

    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;

    let res = client.key_words(guild_id).update(&key_word).await?;

    msg.reply(ctx, format!("updated key word: {}", res.name))
        .await?;

    Ok(())
}

#[command]
#[num_args(0)]
async fn list(ctx: &Context, msg: &Message) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let res = client.key_words(guild_id).list().await?;

    BotUtils::run_paged_menu(ctx, msg, res).await?;

    Ok(())
}

#[command]
#[checks(BOT_ADMIN)]
#[num_args(1)]
async fn delete(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let name = args.single_quoted::<String>()?;
    client.key_words(guild_id).delete(&name).await?;

    msg.reply(ctx, format!("Deleted key_word: {}", name))
        .await?;

    Ok(())
}
