use anyhow::anyhow;
use serenity::framework::standard::Args;

pub struct ArgParser;

impl ArgParser {
    /// Returns the first arg as the key/name and the rest of the args as the
    /// value
    pub fn key_value_pair(mut args: Args) -> anyhow::Result<(String, String)> {
        let name = args.single_quoted::<String>()?;
        let value = args.remains().ok_or(anyhow!("No remaining args"))?;
        Ok((name, value.to_string()))
    }
}
