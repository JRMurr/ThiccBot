use anyhow::anyhow;
use client::key_words::KeyWord;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::channel::Message,
};

use crate::get_thicc_client;

#[group]
#[prefixes(keyWord, keyword, keyword, keyWords, key_word)]
#[commands(create)]
#[summary = "Commands for creating and managing key words"]
#[only_in(guilds)]
pub struct KeyWords; // TODO: add bot admin checks

#[command]
#[aliases("set", "make", "add", "save")]
async fn create(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let name = args.single_quoted::<String>()?;

    // TODO: add some arg validation to reduce the risk of an error
    // https://docs.rs/serenity/0.10.9/serenity/framework/standard/macros/attr.command.html
    let response = args
        .remains()
        .ok_or(anyhow!("No remaining args for response"))?;

    let client = get_thicc_client(ctx).await?;
    // TODO: old thicc bot did not support this but the backend allows multiple
    // responses
    let key_word = KeyWord::new(name, vec![response.to_string()]);

    let res = client
        .key_words()
        .create(msg.guild_id.unwrap().0, &key_word)
        .await?;

    msg.reply(ctx, format!("Created key word: {}", res.name))
        .await?;
    Ok(())
}