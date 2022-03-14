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
#[commands(say, choose, choose_list, meme_text, emoji_text)]
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

fn map_chars<T>(str: &str, char_mapper: fn(char) -> T) -> String
where
    String: FromIterator<T>,
{
    if emojis::lookup(str).is_some() {
        return str.to_string();
    }

    str.chars().into_iter().map(char_mapper).collect()
}

fn char_to_meme(char: char) -> char {
    let meme_value = 0xFEE0 + (char as u32);
    std::char::from_u32(meme_value).unwrap_or(char)
}

fn join_iter<I: IntoIterator<Item = String>>(iterable: I) -> String {
    itertools::intersperse(iterable, " ".to_string()).collect()
}

#[command]
async fn meme_text(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let words = args.raw_quoted();
    let meme_words: String =
        join_iter(words.map(|word| map_chars(word, char_to_meme)));

    msg.channel_id.say(&ctx.http, meme_words).await?;

    Ok(())
}

fn char_to_emoji(char: char) -> String {
    match char {
        'a'..='z' | 'A'..='Z' => format!(":regional_indicator_{char}:"),
        '0' => ":zero:".to_string(),
        '1' => ":one:".to_string(),
        '2' => ":two:".to_string(),
        '3' => ":three:".to_string(),
        '4' => ":four:".to_string(),
        '5' => ":five:".to_string(),
        '6' => ":six:".to_string(),
        '7' => ":seven:".to_string(),
        '8' => ":eight:".to_string(),
        '9' => ":nine:".to_string(),
        _ => char.to_string(),
    }
}

#[command]
async fn emoji_text(ctx: &Context, msg: &Message, args: Args) -> CommandResult {
    let words = args.raw_quoted();
    let emoji_words =
        join_iter(words.map(|word| map_chars(word, char_to_emoji)));
    msg.channel_id.say(&ctx.http, emoji_words).await?;
    Ok(())
}
