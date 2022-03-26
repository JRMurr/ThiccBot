use crate::{error::ThiccError, ThiccClient, ThiccResult};

use core::fmt;

#[derive(Debug, serde::Serialize, serde::Deserialize)]
pub struct Alias {
    pub name: String,
    pub command: String,
}

impl From<(String, String)> for Alias {
    fn from((name, command): (String, String)) -> Self {
        Self { name, command }
    }
}

impl fmt::Display for Alias {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}

pub struct AliasManager<'a> {
    client: &'a ThiccClient,
    guild_route: String,
}

impl AliasManager<'_> {
    pub async fn get(&self, search: &str) -> ThiccResult<Option<Alias>> {
        let res = self
            .client
            .get_json::<Alias, _>(format!("{}/{}", self.guild_route, search))
            .await;
        ThiccClient::swallow_404(res)
    }

    pub async fn list(&self) -> ThiccResult<Vec<Alias>> {
        self.client
            .get_json::<Vec<Alias>, _>(&self.guild_route)
            .await
    }

    pub async fn create(&self, alias: &Alias) -> ThiccResult<Alias> {
        let res = self.client.post_json(&self.guild_route, alias).await;
        ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::BAD_REQUEST {
                Some(ThiccError::ResourceAlreadyExist {
                    name: alias.name.clone(),
                    resource_type: "Alias".to_string(),
                })
            } else {
                None
            }
        })
    }

    pub async fn update(&self, alias: &Alias) -> ThiccResult<Alias> {
        let res = self.client.put_json(
            format!("{}/{}", &self.guild_route, alias.name),
            alias
        ).await;
        ThiccClient::handle_status(res, |status| {
            if status == reqwest::StatusCode::NOT_FOUND {
                Some(ThiccError::ResourceDoesNotExist {
                    name: alias.name.clone(),
                    resource_type: "Alias".to_string(),
                })
            } else {
                None
            }
        })
    }

    pub async fn delete(&self, alias_name: &str) -> ThiccResult<()> {
        self.client
            .delete_helper(format!("{}/{}", self.guild_route, alias_name))
            .await
    }
}

const ALIAS_ROUTE: &str = "alias/discord";

impl ThiccClient {
    pub fn alias(&self, guild_id: u64) -> AliasManager {
        let guild_route = format!("{}/{}", ALIAS_ROUTE, guild_id);
        AliasManager {
            client: self,
            guild_route,
        }
    }
}
