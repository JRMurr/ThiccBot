use client::{key_words::KeyWord, ThiccClient};
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::channel::Message,
};

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
    let response = args.remains().unwrap(); // TODO: add some arg validation https://docs.rs/serenity/0.10.9/serenity/framework/standard/macros/attr.command.html

    let key_word = KeyWord::new(name, vec![response.to_string()]);

    // TODO: need to add thicc client to the context.data so it can be used here

    msg.reply(ctx, format!("key_word: {:?}", key_word)).await?;
    Ok(())
}
