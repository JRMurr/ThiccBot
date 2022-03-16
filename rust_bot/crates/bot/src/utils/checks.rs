use serenity::{
    client::Context,
    framework::standard::{
        macros::check, Args, CommandOptions, CommandResult, Reason,
    },
    model::{guild::Guild, id::RoleId, prelude::Message},
};

use crate::{utils::BotUtils, OwnerHolder};

#[check]
pub async fn bot_admin_check(
    ctx: &Context,
    msg: &Message,
    _: &mut Args,
    _: &CommandOptions,
) -> Result<(), Reason> {
    let data = ctx.data.read().await;

    let bot_owner_id = data.get::<OwnerHolder>().unwrap();

    if msg.author.id.0 == *bot_owner_id {
        // I can do anything
        return Ok(());
    }

    let guild = msg.guild(&ctx.cache).await.ok_or(Reason::Unknown)?;

    if guild.owner_id == msg.author.id {
        // server owner can do anything
        return Ok(());
    }

    // TODO: for all guild and role look ups check if cache will be good?
    // maybe force rest calls if not found?
    let client = BotUtils::get_thicc_client(ctx)
        .await
        .map_err(|_| Reason::Unknown)?;

    let user_roles = match &msg.member {
        Some(member) => &member.roles,
        None => return Err(Reason::Unknown),
    };

    let guild_info = client
        .guilds()
        .get(guild.id.0)
        .await
        .map_err(|_| Reason::Unknown)?
        .ok_or(Reason::Unknown)?;

    let admin_role_id = match guild_info.admin_role {
        Some(id) => RoleId(id).to_role_cached(&ctx.cache).await,
        None => None,
    };

    // TODO: add is guild owner check
    // TODO: go through roles and find if any has manage roles as
    // a default when no admin role is set

    Ok(())
}
