use futures::{stream, stream::StreamExt};
use serenity::{
    client::Context,
    framework::standard::{macros::check, Args, CommandOptions, Reason},
    model::{guild::Role, id::RoleId, prelude::Message, Permissions},
};

use crate::utils::BotUtils;

// TODO: remove all these expects and add http calls if cache not good

#[check]
pub async fn server_owner(
    ctx: &Context,
    msg: &Message,
    _: &mut Args,
    _: &CommandOptions,
) -> Result<(), Reason> {
    let guild = msg.guild(&ctx.cache).await.expect("guild not in cache");

    if guild.owner_id == msg.author.id {
        // server owner can do anything
        return Ok(());
    }
    Err(Reason::Unknown)
}

#[check]
pub async fn bot_admin(
    ctx: &Context,
    msg: &Message,
    _: &mut Args,
    _: &CommandOptions,
) -> Result<(), Reason> {
    let guild = msg.guild(&ctx.cache).await.expect("guild not in cache");

    if guild.owner_id == msg.author.id {
        // server owner can do anything
        return Ok(());
    }

    let client = BotUtils::get_thicc_client(ctx)
        .await
        .map_err(|_| Reason::Unknown)?;

    let user_roles = match &msg.member {
        Some(member) => &member.roles,
        None => return Err(Reason::Unknown),
    };

    let user_roles: Vec<Role> = stream::iter(user_roles)
        .then(|role_id| async move {
            role_id
                .to_role_cached(&ctx.cache)
                .await
                .expect("user role not in cache")
        })
        .collect()
        .await;

    let guild_info = client
        .guilds()
        .get(guild.id.0)
        .await
        .map_err(|_| Reason::Unknown)?
        .ok_or(Reason::Unknown)?;

    match guild_info.admin_role {
        Some(id) => {
            let admin_role = RoleId(id)
                .to_role_cached(&ctx.cache)
                .await
                .expect("admin role not in cache");
            let max_role_pos =
                user_roles.iter().map(|role| role.position).max();
            if max_role_pos.unwrap_or(0) >= admin_role.position {
                Ok(())
            } else {
                Err(Reason::Unknown)
            }
        }
        None => {
            // If no admin role set, just check if they can manage roles
            let user_perms = user_roles
                .iter()
                .fold(Permissions::empty(), |acc, p| acc.union(p.permissions));
            dbg!(user_perms);
            if user_perms.manage_roles() {
                Ok(())
            } else {
                Err(Reason::Unknown)
            }
        }
    }
}
