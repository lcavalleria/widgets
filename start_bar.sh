#!/bin/sh
# if MAIN_MONITOR_NAME is not set, main monitor will be the first of the wayland list.
# MAIN_MONITOR_NAME will be checked by grep, so any substring in wlrctl outputs will work.

IFS=$'\n'
mapfile -t displays_arr < <(wlrctl output list)
main_display=$(printf '%s\n' "${displays_arr[@]}" | grep -n "$MAIN_MONITOR_NAME" | cut -c 1)
eww close bar0
eww close bar1
eww close bar2
if [ ${#displays_arr[@]} -gt 1 ]; then
	if [ $main_display -eq 3 ]; then
		eww open bar2
	elif [ $main_display -eq 2 ]; then
		eww open bar1
	else
		eww open bar0
	fi
else
	eww open bar0
fi
unset IFS
