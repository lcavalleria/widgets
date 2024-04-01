use crate::output_msg::OutputMsg;
use crate::status_icons::StatusIcons;

#[derive(Debug)]
enum EthStatus {
    Connected,
    Disconnected,
}

#[derive(Debug)]
enum WlanStatus {
    Connected,
    Connecting,
    Disconnected,
    Disabled,
}

pub struct NetworkInfo {
    eth_status: EthStatus,
    wlan_status: WlanStatus,
    wlan_name: Option<String>,
}

impl NetworkInfo {
    pub fn create() -> NetworkInfo {
        NetworkInfo {
            eth_status: EthStatus::Disconnected,
            wlan_status: WlanStatus::Disconnected,
            wlan_name: None,
        }
    }

    pub fn update_from_initial_line(&mut self, line: &str) {
        let parts: Vec<&str> = line.split(':').collect();
        let interface = *parts.first().unwrap_or(&"");
        let status = *parts.get(1).unwrap_or(&"");

        match (interface, status) {
            ("eth1", "connected") => self.eth_status = EthStatus::Connected,
            ("wlan0", "connected") => {
                self.wlan_status = WlanStatus::Connected;
                self.wlan_name = Some(parts.get(2).unwrap_or(&"Unknown").to_string());
            }
            ("wlan0", "unavailable") => self.wlan_status = WlanStatus::Disabled,
            (_, _) => (),
        };
    }

    pub fn update_from_monitor_line(&mut self, line: String) {
        let parts: Vec<&str> = line.split(':').collect();

        let interface = *parts.first().unwrap_or(&"");
        let status = parts.get(1).unwrap_or(&"").trim_start();
        let status_first_word = *status
            .split_whitespace()
            .collect::<Vec<&str>>()
            .first()
            .unwrap_or(&"");

        match (interface, status_first_word) {
            ("eth1", "connected") => self.eth_status = EthStatus::Connected,
            ("eth1", "unavailable") => self.eth_status = EthStatus::Disconnected,
            ("wlan0", "using") => {
                let connection_name = status
                    .split(' ')
                    .collect::<Vec<&str>>()
                    .get(2)
                    .unwrap_or(&"Error")
                    .trim_matches('\'');

                self.wlan_name = Some(connection_name.to_string());
            }
            ("wlan0", "connecting") => self.wlan_status = WlanStatus::Connecting,
            ("wlan0", "connected") => self.wlan_status = WlanStatus::Connected,
            ("wlan0", "unavailable") => {
                self.wlan_status = WlanStatus::Disabled;
                self.wlan_name = None;
            }
            ("wlan0", "disconnected") => {
                self.wlan_status = WlanStatus::Disconnected;
                self.wlan_name = None;
            }
            (_, _) => (),
        };
    }

    pub fn format_output_msg(&self) -> OutputMsg {
        let wlan_name = &self.wlan_name.as_deref().unwrap_or("Unknown");
        match (&self.eth_status, &self.wlan_status) {
            (EthStatus::Connected, _) => OutputMsg {
                icon: StatusIcons::ETHERNET,
                text: "Connected".to_string(),
            },
            (EthStatus::Disconnected, WlanStatus::Connected) => OutputMsg {
                icon: StatusIcons::WLAN_CONNECTED,
                text: wlan_name.to_string(),
            },
            (EthStatus::Disconnected, WlanStatus::Connecting) => OutputMsg {
                icon: StatusIcons::WLAN_CONNECTING,
                text: wlan_name.to_string(),
            },
            (EthStatus::Disconnected, WlanStatus::Disabled) => OutputMsg {
                icon: StatusIcons::WLAN_DISABLED,
                text: "Disabled".to_string(),
            },
            (EthStatus::Disconnected, WlanStatus::Disconnected) => OutputMsg {
                icon: StatusIcons::DISCONNECTED,
                text: "Disconnected".to_string(),
            },
        }
    }
}
