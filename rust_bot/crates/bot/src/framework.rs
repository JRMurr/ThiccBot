use client::error::ClientErrors;
use serenity::{
    client::Context,
    framework::standard::{
        macros::{help, hook},
        Args, CommandGroup, CommandResult, HelpOptions, StandardFramework,
    },
    model::channel::Message,
};

use crate::commands::key_words::KEYWORDS_GROUP;
use std::collections::HashSet;

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

pub fn create_framework() -> StandardFramework {
    // TODO: look into https://docs.rs/serenity/0.10.9/serenity/framework/standard/struct.Configuration.html#method.dynamic_prefix
    // to be able to set the prefix per server
    StandardFramework::new()
        .configure(|c| c.prefix("?"))
        .after(after) // set the bot's prefix to "?"
        .help(&MY_HELP)
        .group(&KEYWORDS_GROUP)
}
