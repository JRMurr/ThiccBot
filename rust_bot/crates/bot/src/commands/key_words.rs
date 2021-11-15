use anyhow::anyhow;
use client::{error::ThiccError, key_words::KeyWord};
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::channel::Message,
};

struct ErrorWrapper {
    err: serenity::framework::standard::CommandError,
}

impl From<ErrorWrapper> for serenity::framework::standard::CommandError {
    fn from(e: ErrorWrapper) -> Self {
        e.err
    }
}

impl From<anyhow::Error> for ErrorWrapper {
    fn from(e: anyhow::Error) -> Self {
        match e.downcast::<ThiccError>() {
            Ok(thicc_err) => Self {
                err: thicc_err.into(),
            },
            Err(err) => Self { err: err.into() },
        }
    }
}

use crate::utils::BotUtils;

#[group]
#[prefixes(keyWord, keyword, keyword, keyWords, key_word)]
#[commands(create, list)]
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

    // TODO: old thicc bot did not support this but the backend allows multiple
    // responses
    let key_word = KeyWord::new(name, vec![response.to_string()]);

    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;

    // TODO: handle already existing (400)
    let res = client.key_words(guild_id).create(&key_word).await?;

    msg.reply(ctx, format!("Created key word: {}", res.name))
        .await?;

    Ok(())
}

#[command]
async fn list(ctx: &Context, msg: &Message) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let res = client.key_words(guild_id).list().await?;
    // TODO: add emoji based pagination like old bot
    // this lib might help https://github.com/AriusX7/serenity-utils
    msg.reply(ctx, format!("{:?}", res)).await?;
    Ok(())
}
