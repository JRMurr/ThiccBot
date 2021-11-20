use client::{error::ClientErrors, ThiccResult};

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
    model::channel::Message,
};

use crate::{
    commands::{alias::ALIASES_GROUP, key_words::KEYWORDS_GROUP},
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

        let prefix = "?";
        if msg.content.starts_with(prefix) {
            if let Some(alias_name) = msg.content.strip_prefix(prefix) {
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
            if let Some(client_error) = why.downcast_ref::<ClientErrors>() {
                match client_error {
                    ClientErrors::Thicc(thicc_error) => {
                        let _ =
                            msg.reply(ctx, format!("{}", thicc_error)).await;
                        ()
                    }
                    _ => (),
                };
            }
        }
    }
}

#[hook]
async fn dispatch_error_hook(
    _context: &Context,
    msg: &Message,
    error: DispatchError,
) {
    // TODO: probably only do this in dev
    error!("Dispatch Error for msg: {:?}, error: {:?}", msg, error);
}

// #[hook]
// async fn normal_message(_ctx: &Context, msg: &Message) {
//     // TODO: probably only do this in dev
//     // TODO: could also just do the manual call to dispatch here instead of
//     // making my own framework
//     // println!("Message is not a command '{}'", msg.content);
// }

pub fn create_framework() -> ThiccFramework {
    // TODO: look into https://docs.rs/serenity/0.10.9/serenity/framework/standard/struct.Configuration.html#method.dynamic_prefix
    // to be able to set the prefix per server
    let standard = StandardFramework::new()
        .configure(|c| c.prefix("?"))
        .after(after) // set the bot's prefix to "?"
        .help(&MY_HELP)
        .on_dispatch_error(dispatch_error_hook)
        // .normal_message(normal_message)
        .group(&KEYWORDS_GROUP)
        .group(&ALIASES_GROUP);
    ThiccFramework { standard }
}
