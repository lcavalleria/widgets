# TODO: THIS SCRIPT IS CRAP. IT WILL BE REPLACED by the network_monitor rust directory.
# To be used as deflisten network widget.
# TODO (BROKEN ATM): Decouple initial status and events:
#   Fix the wlan_outputs and eth_outputs functions. Some variables are not present.
#   Split process_line to process_status_line and process_event_line.
#   The outputs of those functions should stay the same.
#   Maybe tree aproach? (device -> state -> name?)
import subprocess
import datetime
import sys

debugging = True


def debug(msg):
    if debugging == True:
        with open("/var/log/debug", "a") as debugfile:
            debugfile.write("[" + str(datetime.datetime.now()) + "] - network_monitor.py: " + msg + "\n")


def generate_output(icon, display_text):
    debug("generate eth output string")
    output = "{\"icon\":\"" + icon + "\",\"text\":\"" + display_text +"\"}"
    debug("output string (eth): " + output)
    return output


def wlan_outputs(state, wlan_name):
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
        if wlan_name: # running "nmcli device status", not monitor
            connection_name = wlan_name
        icon = "直"
        display_text = connection_name
    else:
        icon = ""
        display_text = "WTF wlan0"
    return icon, display_text

def eth_outputs(state):
    icon = "﴿"
    if (state.startswith("connected")):
        debug("ethX is connected")
        display_text = "Ethernet"
    elif (state.startswith("disconnected")):
        debug("ethX is disconnected")
        display_text = "Disconnected"
    elif (state.startswith("using") or state.startswith("connecting")):
        debug("ethX is connecting")
        display_text = "Connecting"
    elif (state.startswith("unavailable")):
        debug("ethX is unavailable.")
        display_text = "Disabled"
    else:
        debug(f"something strange. device: {device}, state: {state}")
        icon = ""
        display_text = "WTF eth1"
    return icon, display_text


def process_line(line):
    e = line.split(":")
    debug("event info: " + str(e))
    device = e[0]
    debug("device: " + str(device))
    state = e[1].strip(' ').strip('\n')
    debug("state: " + str(state))
    wlan_name = None
    if len(e) == 3:
        wlan_name = e[2].strip('\n')


    if (device == "wlan0"):
        debug("device is wlan0")
        icon, display_text = wlan_outputs(state, wlan_name)
    elif (device.startswith("eth")):
        debug("device is: " + device + " (starts with \"eth\")")
        icon, display_text = eth_outputs(state)
    else:
        return None
    return icon, display_text

def print_nmcli_status_to_eww(process):
    events = []
    for line in process.stdout:
        debug("reading line")
        if not line:
            debug("NO LINE, BREAKING")
            break
        ic_txt = process_line(line)
        if ic_txt is not None:
            events.append(ic_txt)
    output = None
    for event in events:
        if event[1] == "Ethernet":
            output = generate_output(event[0], event[1])
    if output is None:
        output = generate_output(events[0][0], events[0][1])

    print(output, flush=True)

def print_nmcli_events_to_eww(process):
    for line in process.stdout:
        debug("reading line")
        if not line:
            debug("NO LINE, BREAKING")
            break
        ic_txt = process_line(line)
        if ic_txt is not None:
            output = generate_output(ic_txt[0], ic_txt[1])
            print(output, flush=True)



# do a first run when script start
process = subprocess.Popen(["nmcli", "-g", "device, state, connection", "device", "status"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print_nmcli_status_to_eww(process)


# and start processing nmcli monitor outputs
process = subprocess.Popen(["nmcli", "device", "monitor"], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print_nmcli_events_to_eww(process)

