# To be used as deflisten network widget.

import subprocess
import sys

process = subprocess.Popen(["nmcli", "device", "monitor"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    else:
        icon = "﴿"
        display_text = "Ethernet"

    arg = sys.argv[1]
    if (arg == "icon"):
        print(icon, flush=True)
    elif (arg == "text"):
        print(display_text, flush=True)
    else:
        print("Fix the arg!", flush=True)
