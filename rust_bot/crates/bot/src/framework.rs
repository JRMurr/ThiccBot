use client::{
    error::{ClientErrors, ThiccError},
    ThiccResult,
};

use serenity::{
    async_trait,
    client::Context,
    framework::{
        standard::{
            macros::{help, hook},
            Args, CommandGroup, CommandResult, DispatchError, HelpOptions,
            StandardFramework,
        },
        Framework,
    },
    model::{channel::Message, id::UserId},
};

use crate::{
    commands::{
        admin::ADMIN_GROUP, alias::ALIASES_GROUP, key_words::KEYWORDS_GROUP,
        last_fm::LASTFM_GROUP, misc::MISC_GROUP, quotes::QUOTES_GROUP,
    },
    utils::BotUtils,
};

use std::collections::HashSet;

pub struct ThiccFramework {
    standard: StandardFramework,
}

impl ThiccFramework {
    async fn my_dispatch(&self, ctx: Context, msg: Message) -> ThiccResult<()> {
        let (client, guild_id) = BotUtils::get_info(&ctx, &msg).await?;
        // TODO: the parse struct is not public need to remake
        // https://github.com/serenity-rs/serenity/blob/current/src/framework/standard/parse/mod.rs#L218

        let prefixes = get_command_prefixes(&ctx, &msg).await?;
        for prefix in prefixes {
            if let Some(alias_name) = msg.content.strip_prefix(&prefix) {
                // TODO: check alias_name not a built in command
                if let Some(alias) =
                    client.alias(guild_id).get(alias_name).await?
                {
                    let mut cloned_msg = msg.clone();
                    cloned_msg.content =
                        format!("{}{}", prefix, alias.command.trim());
                    self.standard.dispatch(ctx, cloned_msg).await;
                    return Ok(());
                }
            }
        }
        self.standard.dispatch(ctx, msg).await;

        Ok(())
    }
}

#[async_trait]
impl Framework for ThiccFramework {
    async fn dispatch(&self, ctx: Context, msg: Message) {
        let res = self.my_dispatch(ctx, msg).await;
        if let Err(e) = res {
            error!("my dispatch returned error {:?}", e);
        }
    }
}

#[help]
async fn my_help(
    context: &Context,
    msg: &Message,
    args: Args,
    help_options: &'static HelpOptions,
    groups: &[&'static CommandGroup],
    owners: HashSet<serenity::model::id::UserId>,
) -> CommandResult {
    let _ = serenity::framework::standard::help_commands::with_embeds(
        context,
        msg,
        args,
        help_options,
        groups,
        owners,
    )
    .await;
    Ok(())
}

#[hook]
async fn after(
    ctx: &Context,
    msg: &Message,
    command_name: &str,
    command_result: CommandResult,
) {
    match command_result {
        Ok(()) => trace!("Processed command '{}'", command_name),
        Err(why) => {
            // Only use backtraces on nightly
            #[cfg(nightly)]
            {
                // print a backtrace if available
                use std::backtrace::BacktraceStatus;
                let bt = err.backtrace();
                if bt.status() == BacktraceStatus::Captured {
                    eprintln!("{}", bt);
                }
            }
            error!("Command '{}' returned error {:?}", command_name, why);
            if let Some(ClientErrors::Thicc(thicc_error)) =
                why.downcast_ref::<ClientErrors>()
            {
                // show thicc errors wrapped in clientErrors
                let _ = msg.reply(ctx, format!("{}", thicc_error)).await;
            } else if let Some(thicc_error) = why.downcast_ref::<ThiccError>() {
                // show unwrapped thicc errors
                let _ = msg.reply(ctx, format!("{}", thicc_error)).await;
            }
        }
    }
}

/// Get configured command prefix for the guild
async fn get_command_prefixes(
    ctx: &Context,
    msg: &Message,
) -> anyhow::Result<Vec<String>> {
    let (client, guild_id) = BotUtils::get_info(ctx, msg).await?;
    let guild = client.guilds().get(guild_id).await?;
    Ok(match guild {
        Some(g) => g.command_prefixes.unwrap_or_default(),
        None => Vec::new(),
    })
}

#[hook]
async fn dispatch_error_hook(
    _context: &Context,
    msg: &Message,
    error: DispatchError,
) {
    error!("Dispatch Error for msg: {:?}, error: {:?}", msg, error);
}

// #[hook]
// async fn normal_message(_ctx: &Context, msg: &Message) {
//     // TODO: probably only do this in dev
//     // TODO: could also just do the manual call to dispatch here instead of
//     // making my own framework
//     println!("Message is not a command '{}'", msg.content);
// }

pub fn create_framework(
    owner_id: UserId,
    bot_user_id: Option<UserId>,
) -> ThiccFramework {
    let mut owner_set = HashSet::new();
    owner_set.insert(owner_id);
    let standard = StandardFramework::new()
        .configure(|c| {
            c.on_mention(bot_user_id)
                .prefix("?")
                .owners(owner_set)
                .dynamic_prefix(|ctx, msg| {
                    Box::pin(async move {
                        let prefixes = get_command_prefixes(ctx, msg)
                            .await
                            .unwrap_or_default();
                        // TODO: dynamic_prefix can only return a single prefix
                        // at a time
                        prefixes.get(0).cloned()
                    })
                })
        })
        .after(after)
        .help(&MY_HELP)
        .on_dispatch_error(dispatch_error_hook)
        // .normal_message(normal_message)
        .group(&KEYWORDS_GROUP)
        .group(&ALIASES_GROUP)
        .group(&MISC_GROUP)
        .group(&LASTFM_GROUP)
        .group(&QUOTES_GROUP)
        .group(&ADMIN_GROUP);
    ThiccFramework { standard }
}
