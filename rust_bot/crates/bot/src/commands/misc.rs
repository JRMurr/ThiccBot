use rand::seq::{IteratorRandom, SliceRandom};
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

#[group]
#[commands(say, choose, choose_list, meme_text)]
pub struct Misc;

#[command]
async fn say(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    msg.channel_id.say(&ctx.http, args.rest()).await?;

    Ok(())
}

#[command]
async fn choose(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let answer = args
        .raw_quoted()
        .choose(&mut rand::thread_rng())
        .unwrap_or("No options passed");
    msg.channel_id.say(&ctx.http, answer).await?;

    Ok(())
}

#[command]
async fn choose_list(
    ctx: &Context,
    msg: &Message,
    args: Args,
) -> CommandResult {
    let mut list: Vec<_> = args.raw_quoted().collect();
    list.shuffle(&mut rand::thread_rng());

    // TODO: make this look nicer
    let res = format!("{:?}", list);

    msg.channel_id.say(&ctx.http, res).await?;

    Ok(())
}

fn char_to_meme(char: char) -> char {
    let meme_value = 0xFEE0 + (char as u32);
    std::char::from_u32(meme_value).unwrap_or(char)
}

fn map_to_meme_text(str: &str) -> String {
    if emojis::lookup(str).is_some() {
        return str.to_string();
    }

    str.chars().into_iter().map(char_to_meme).collect()
}

#[command]
async fn meme_text(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let words = args.raw_quoted();
    // TODO: better join https://docs.rs/itertools/latest/itertools/trait.Itertools.html#method.intersperse
    let emoji_words: Vec<_> = words.map(map_to_meme_text).collect();

    msg.channel_id.say(&ctx.http, emoji_words.join(" ")).await?;

    Ok(())
}
