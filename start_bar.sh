#!/bin/sh

#user=$(whoami)
# export necessary variables to call eww daemon and + wlrctl
#export XDG_RUNTIME_DIR="/run/user/$(id -u $user)"
#export XDG_CONFIG_HOME="/home/$user/.config"
#export WAYLAND_DISPLAY="wayland-1"
### 
displays=$(wlrctl output list | wc -l)
eww close bar1
eww close bar0
if [ $displays -gt 1 ]; then
	eww open bar1
else
	eww open bar0
fi
