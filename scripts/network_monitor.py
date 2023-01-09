# To be used as deflisten network widget.

import subprocess
import sys

process = subprocess.Popen(["nmcli", "device", "monitor"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

wlan_prev_icon = ""
wlan_prev_text = ""

for line in process.stdout:
    if not line: break
    e = line.split(":")
    device = e[0]
    state = e[1].strip(' ').strip('\n')

    if (device == "wlan0"):
        if (state.startswith("unavailable")):
            icon = ""
            display_text = "Disabled"
            connection_name = ""
        elif (state.startswith("disconnected")):
            icon = "睊"
            display_text = "Disconnected"
            connection_name = ""
        elif (state.startswith("using")):
            connection_name = state.split('\'', 1)[1][:-1]
            icon = "直"
            display_text = "[[{name}]]".format(name=connection_name)
        elif (state.startswith("connecting")):
            icon = "直"
            display_text = "[[{name}]]".format(name=connection_name)
        elif (state.startswith("connected")):
            icon = "直"
            display_text = connection_name
        else:
            icon = ""
            display_text = "WTF wlan0"
        wlan_prev_icon = icon
        wlan_prev_text = display_text
    elif (device == "eth1"):
        if (state.startswith("disconnected")):
            icon = ""
            display_text = "[[Ethernet]]"
        elif (state.startswith("connected")):
            icon = "﴿"
            display_text = "Ethernet"
        elif (state.startswith("using") or state.startswith("connecting")):
            icon = "﴿"
            display_text = "Connecting"
        elif (state.startswith("unavailable")):
            icon = wlan_prev_icon
            display_text = wlan_prev_text
        else:
            icon = ""
            display_text = "WTF eth1"

    print("{\"icon\":\"" + icon + "\",\"text\":\"" + display_text +"\"}", flush=True)

