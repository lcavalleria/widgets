#!/bin/sh

case "$1" in
	"volumeUp")
		(pamixer -i 5 && eww update volume=$(pamixer --get-volume)) &
		;;
	"volumeDown")
		(pamixer -d 5 && eww update volume=$(pamixer --get-volume)) &
		;;
	"mute")
		(pamixer -t && eww update muted=$(pamixer --get-mute)) &
		;;
esac
