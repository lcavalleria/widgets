#!/bin/bash
#
# Run eww update after setting the variable to find the daemon.
# Called from /usr/lib/udev/run-users-script
#
###########

user=$(whoami)
# necessary to call eww daemon
export XDG_RUNTIME_DIR="/run/user/$(id -u $user)"
case "$1" in
	"charging")
		eww update batteryCharging=$2
		;;
	"present")
		eww update batteryPresent=$2
		;;
esac
