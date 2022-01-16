#!/bin/bash
# This script listens to bluetoothctl and outputs the changes of Powered and Discoverable
# To be used in eww as a deflisten

as_boolean () {
	case "$1" in
		"yes")
			echo "true"
			;;
		"no")
			echo "false"
			;;
	esac
}

get_state () {
	res=$(bluetoothctl show | grep -E "^	$1" | awk '{ print $2 }')
	as_boolean $res
}

case "$1" in
	"enabled")
		get_state "Powered"
		sleep infinity | bluetoothctl \
		| grep --line-buffered "Powered" \
		| while read -r; do 
			get_state "Powered"
		done
		;;
	"discoverable")
		get_state "Discoverable"
		sleep infinity | bluetoothctl \
		| grep --line-buffered "Discoverable" \
		| while read -r a b c d e f g h i j k; do 
			get_state "Discoverable"
		done
		;;
esac
