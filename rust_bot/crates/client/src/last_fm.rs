use std::borrow::Cow;

use crate::{error::ThiccError, ErrorMap, ThiccClient, ThiccResult};

pub struct LastFmManager<'a> {
    client: &'a ThiccClient,
}

impl LastFmManager<'_> {
    // TODO: make period an enum
    pub async fn get_grid<'a>(
        &self,
        user: &str,
        period: &str,
    ) -> ThiccResult<Cow<'a, [u8]>> {
        todo!()
        // let res = self.client.get_bytes(format(""))
    }
}
