use super::BotUtils;
use serenity::{
    builder::CreateMessage,
    client::Context,
    model::prelude::{Message, Reaction, ReactionType},
};
use serenity_utils::menu::*;
use std::{fmt::Display, sync::Arc};

// A custom function to be used as a control function for the menu.
async fn first_page<'a>(menu: &mut Menu<'a>, reaction: Reaction) {
    // Remove the reaction used to change the menu.
    let _ = &reaction.delete(&menu.ctx.http).await;

    // Set page number to `0`.
    menu.options.page = 0;
}

// A custom function to be used as a control function for the menu.
async fn last_page<'a>(menu: &mut Menu<'a>, reaction: Reaction) {
    // Remove the reaction used to change the menu.
    let _ = &reaction.delete(&menu.ctx.http).await;

    // Set page number to total - 1.
    menu.options.page = menu.pages.len() - 1;
}

fn get_pages<'a, T: Display>(
    entries: Vec<T>,
    page_size: usize,
) -> Vec<CreateMessage<'a>> {
    // TODO: would be nice to add a number to show with each entry
    entries
        .chunks(page_size)
        .map(|chunk| {
            chunk.iter().fold("".to_string(), |acc, entry| {
                format!("{}\n{}", acc, entry)
            })
        })
        .map(|description| {
            let mut page = CreateMessage::default();
            page.content("").embed(|e| {
                e.description(description);

                e
            });
            page
        })
        .collect()
}

impl BotUtils {
    pub async fn run_paged_menu<T: Display>(
        ctx: &Context,
        msg: &Message,
        entries: Vec<T>,
    ) -> Result<Option<Message>, anyhow::Error> {
        // let stop_reaction = ReactionType::try_from("⏹️")?;
        if entries.len() == 0 {
            let msg = msg.reply(ctx, "No entries to list").await?;
            return Ok(Some(msg));
        }
        let controls = vec![
            Control::new(
                ReactionType::from('⏪'),
                Arc::new(|m, r| Box::pin(first_page(m, r))),
            ),
            Control::new(
                ReactionType::from('◀'),
                Arc::new(|m, r| Box::pin(prev_page(m, r))),
            ),
            Control::new(
                ReactionType::try_from("⏹️")?, //⏹️
                Arc::new(|m, r| Box::pin(close_menu(m, r))),
            ),
            Control::new(
                ReactionType::from('▶'),
                Arc::new(|m, r| Box::pin(next_page(m, r))),
            ),
            Control::new(
                ReactionType::from('⏩'),
                Arc::new(|m, r| Box::pin(last_page(m, r))),
            ),
        ];

        let options = MenuOptions {
            controls,
            timeout: 60.0, // in seconds
            ..Default::default()
        };

        let pages = get_pages(entries, 10);
        let menu = Menu::new(ctx, msg, &pages, options);
        let msg = menu.run().await?;
        Ok(msg)
    }
}
