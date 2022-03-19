use crate::utils::{checks::SERVER_OWNER_CHECK, BotUtils};
use client::guilds::PrefixType;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{command, group},
        Args, CommandResult,
    },
    model::{id::RoleId, prelude::Message},
};

#[group]
#[prefixes(admin)]
#[commands(set_bot_admin, add_prefix)]
#[summary = "Commands for managing thicc bot in this server"]
#[only_in(guilds)]
pub struct Admin;

#[command]
#[checks(SERVER_OWNER)]
#[num_args(1)]
async fn set_bot_admin(
    ctx: &Context,
    msg: &Message,
    mut args: Args,
) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    // TODO: use https://docs.rs/serenity/latest/serenity/utils/trait.ArgumentConvert.html#tymethod.convert ?
    let role_id = args.single_quoted::<RoleId>()?.0;
    client.guilds().set_bot_admin(guild_id, role_id).await?;

    msg.reply(ctx, format!("set admin role to: {}", args.message()))
        .await?;

    Ok(())
}
#[command]
#[num_args(2)]
async fn add_prefix(
    ctx: &Context,
    msg: &Message,
    mut args: Args,
) -> CommandResult {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let prefix_type = args.single_quoted::<PrefixType>()?;
    let prefix = args.single_quoted::<String>()?;
    client
        .guilds()
        .create_prefix(guild_id, &prefix_type, &prefix)
        .await?;

    msg.reply(
        ctx,
        format!(
            "({prefix}) has been added to the list of possible {prefix_type}es"
        ),
    )
    .await?;

    Ok(())
}
