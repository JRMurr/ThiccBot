use crate::{error::ThiccError, ThiccClient, ThiccResult};
use bytes::Buf;
use std::{borrow::Cow, io::Read, str::FromStr};
use strum::{Display, EnumVariantNames, VariantNames};

pub struct LastFmManager<'a> {
    client: &'a ThiccClient,
}

#[derive(Display, Debug, PartialEq, EnumVariantNames)]
pub enum Period {
    #[strum(to_string = "overall")]
    Overall,
    #[strum(to_string = "7day")]
    SevenDays,
    #[strum(to_string = "1month")]
    OneMonth,
    #[strum(to_string = "3month")]
    ThreeMonths,
    #[strum(to_string = "6month")]
    SixMonths,
    #[strum(to_string = "12month")]
    TwelveMonths,
}

impl Default for Period {
    fn default() -> Self {
        Self::SevenDays
    }
}

// Would use strum EnumString but want a better error message
impl FromStr for Period {
    type Err = ThiccError;
    fn from_str(s: &str) -> Result<Period, ThiccError> {
        match s.trim() {
            "" => Ok(Period::default()),
            "overall" | "all time" => Ok(Period::Overall),
            "7day" | "7 days" => Ok(Period::SevenDays),
            "1month" | "1 month" => Ok(Period::OneMonth),
            "3month" | "3 months" => Ok(Period::ThreeMonths),
            "6month" | "6 months" => Ok(Period::SixMonths),
            "12month" | "12 months" => Ok(Period::TwelveMonths),
            _ => Err(ThiccError::ParseError {
                allowed: Period::VARIANTS,
                got: s.to_string(),
            }),
        }
    }
}

impl LastFmManager<'_> {
    pub async fn get_grid<'a>(
        &self,
        user: String,
        period: Period,
    ) -> ThiccResult<Cow<'a, [u8]>> {
        let path = format!("lastFM/grid/{user}/{period}");
        let res = self.client.get_bytes(path).await?;
        let mut reader = res.reader();
        let mut buf: Vec<u8> = Vec::new();
        let _ = reader.read_to_end(&mut buf)?;
        Ok(Cow::from(buf))
    }
}

impl ThiccClient {
    pub fn last_fm(&self) -> LastFmManager {
        LastFmManager { client: self }
    }
}
