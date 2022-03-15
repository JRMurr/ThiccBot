use client::last_fm::Period;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    http::AttachmentType,
    model::prelude::Message,
};

use crate::utils::{ArgParser, BotUtils};

#[group]
#[prefixes(lastfm, last_fm, lastFm)]
#[commands(grid)]
pub struct LastFm;

#[command]
#[min_args(1)]
#[max_args(2)]
async fn grid(ctx: &Context, msg: &Message, mut args: Args) -> CommandResult {
    let http = &ctx.http;
    let channel_id = msg.channel_id;
    let typing = channel_id.start_typing(http)?;

    let thicc_client = BotUtils::get_thicc_client(ctx).await?;

    let user_name = args.single_quoted::<String>()?;
    let period = ArgParser::parse_with_default::<Period>(args)?;

    let image = thicc_client.last_fm().get_grid(user_name, period).await?;
    let attachment = AttachmentType::Bytes {
        data: image,
        filename: "image.jpeg".to_string(),
    };

    channel_id
        .send_files(http, vec![attachment], |m| m.reference_message(msg))
        .await?;

    typing.stop();
    Ok(())
}
