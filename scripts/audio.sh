#!/bin/bash
# This script reads the pactl subscribe and outputs the volume at every change
# To be used in eww as a deflisten

case "$1" in
	"volume")
		pamixer --get-volume; 
		pactl subscribe \
		| grep --line-buffered "Event 'change' on sink " \
		| while read -r; do 
			pamixer --get-volume | cut -d " " -f1;
		done
		;;
	"muted")
		pamixer --get-mute; 
		pactl subscribe \
		| grep --line-buffered "Event 'change' on sink " \
		| while read -r; do 
			pamixer --get-mute | cut -d " " -f1;
		done
		;;
esac	
