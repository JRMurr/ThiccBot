#[cfg(test)]
#[macro_use]
extern crate assert_matches;

pub mod error;
pub mod managers;
pub mod thicc_client;

pub use managers::*;
pub use thicc_client::{ThiccClient, ThiccResult};
