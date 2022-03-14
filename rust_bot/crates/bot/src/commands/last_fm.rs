use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::prelude::Message,
};

use crate::utils::BotUtils;

#[group]
#[prefixes(lastfm, last_fm, lastFm)]
#[commands(grid)]
pub struct LastFm;

#[command]
#[num_args(2)]
async fn grid(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let http = &ctx.http;
    let channel_id = msg.channel_id;
    let typing = channel_id.start_typing(http)?;

    let thicc_client = BotUtils::get_thicc_client(ctx).await?;

    let user_name = args.single_quoted::<String>()?;
    let period = args.single_quoted::<String>()?;
    typing.stop();
    Ok(())
}
