#!/bin/bash
# This script is not called automatically.
# Called from /usr/lib/NetworkManager/dispatcher.d/99-user-scripts
# See https://unix.stackexchange.com/a/538955

user=$(whoami)
# necessary to call eww daemon
export XDG_RUNTIME_DIR="/run/user/$(id -u $user)"
if [ "$2" = "connectivity-change" ]; then
	case "$CONNECTIVITY_STATE" in
		NONE)
			eww update networkDevice=""
			wifiState=$(nmcli -c no radio wifi)
			case "$wifiState" in
				enabled)
					eww update networkName="Disconnected"
					;;
				disabled)
					eww update networkName="Disabled"
					;;
			esac
			;;
		FULL)
			device=$(nmcli -t connection show --active | awk -F: '{ print $4 }')
			eww update networkDevice=$device
			;;
	esac
fi
if [ "$1" = "wlan0" ]; then
	eww update networkName="$CONNECTION_ID"
elif [ "$1" = "eth0" ]; then
	eww update networkName="$IP4_ADDRESS"
fi
