#[macro_use]
extern crate log;

#[tokio::main]
async fn main() {
    env_logger::init();
    info!("Starting Bot");
    let mut client = bot::build_bot().await;
    // start listening for events by starting a single shard
    if let Err(why) = client.start().await {
        error!("An error occurred while running the client: {:?}", why);
    }
}
