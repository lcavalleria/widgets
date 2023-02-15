# To be used as deflisten network widget.

import subprocess
import sys


wlan_prev_icon = ""
wlan_prev_text = ""

def print_nmcli_to_eww(process):
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
                if (len(e) == 3): # running "nmcli device status", not monitor
                    connection_name=e[2].strip('\n')
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



# do a first run when script start
process = subprocess.Popen(["nmcli", "-g", "device, state, connection", "device", "status"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print_nmcli_to_eww(process)


# and start processing nmcli monitor outputs
process = subprocess.Popen(["nmcli", "device", "monitor"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print_nmcli_to_eww(process)

