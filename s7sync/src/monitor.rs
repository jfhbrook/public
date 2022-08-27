use tokio::sync::{mpsc, oneshot, broadcast, watch};
use tokio::task;
use log::{debug, info};

async fn monitor() {
    let (tx_cmd, mut rx_cmd) = mpsc::channel(32);
    let tx_monitor = tx_cmd.clone();
    let tx_config = tx_cmd.clone();

    let (tx_event, mut rx_event) = watch::channel(32);
    let rx_log = rx_event.clone();

    // monitor
    tokio::spawn(async move {
        while let Some(message) = rx_cmd.recv().await {
            // tx_event.send("hi").await;
        }
    });

    // clock
    tokio::spawn(async move {
        tx_monitor.send("monitor").await;
    });

    // config file watcher
    tokio::spawn(async move {
        // task::spawn_blocking(move || { }).await?;
        tx_config.send("reload").await;
    });

    // server-side logging
    tokio::spawn(async move {
        /*
        while let Some(event) = rx_log.recv().await {
            info!("{:?}", event);
        }
        */
    });

    (tx_cmd, rx_event)
}
