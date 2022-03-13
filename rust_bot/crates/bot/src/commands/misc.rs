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
#[commands(say, choose, choose_list)]
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
