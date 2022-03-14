use crate::{ThiccClient, ThiccResult};
use bytes::Buf;
use std::{borrow::Cow, io::Read};
use strum::{Display, EnumString};

pub struct LastFmManager<'a> {
    client: &'a ThiccClient,
}

// TODO: strum errors are lacking, do it myself
#[derive(Display, Debug, PartialEq, EnumString)]
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

impl LastFmManager<'_> {
    // TODO: make period an enum
    pub async fn get_grid<'a>(
        &self,
        user: String,
        period: Option<String>,
    ) -> ThiccResult<Cow<'a, [u8]>> {
        let prefix = "lastFM/grid";
        let path = match period {
            Some(period) => {
                let period = period.parse::<Period>()?;
                format!("{prefix}/{user}/{period}")
            }
            None => format!("{prefix}/{user}"),
        };
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
