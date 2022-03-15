use std::str::FromStr;

use anyhow::anyhow;
use serenity::framework::standard::{ArgError, Args};

pub struct ArgParser;

impl ArgParser {
    /// Returns the first arg as the key/name and the rest of the args as the
    /// value
    pub fn key_value_pair(mut args: Args) -> anyhow::Result<(String, String)> {
        let name = args.single_quoted::<String>()?;
        let value =
            args.remains().ok_or_else(|| anyhow!("No remaining args"))?;
        Ok((name, value.to_string()))
    }

    pub fn parse_with_default<T: FromStr + Default>(
        mut args: Args,
    ) -> Result<T, T::Err> {
        match args.single_quoted::<T>() {
            Ok(val) => Ok(val),
            Err(ArgError::Parse(e)) => Err(e),
            _ => Ok(T::default()),
        }
    }
}
