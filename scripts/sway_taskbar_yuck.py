# Generate a yuck string with the contents of the taskbar
# To be used as deflisten literal from the tasks widget.

import subprocess
import sys
import json

class Task:
    def __init__(self, app_id, focused):
        self.app_id = app_id
        self.focused = focused

    def make_widget(self):
        if (self.focused == True):
            css_class = "taskfocused"
        else:
            css_class = "task"
        return("(box :class '{css_class}' :width 26 :halign 'center' (label :limit-width 1 :show-truncated false :text '{app_id}'))".format(css_class=css_class, app_id=self.app_id))


tasks = dict()

command = "swaymsg -rmt subscribe '[ \"window\" ]'"
with subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
    while True:
        line = process.stdout.readline()
        if not line: break
        t = json.loads(line)
        id = t["container"]["id"]
        app_id = str(t["container"]["app_id"])
        focused = t["container"]["focused"]
        change = t["change"]
        if (change == "close"):
            tasks.pop(id)
        elif (change == "focus"):
            for task in tasks.values(): task.focused = False
            tasks[id] = Task(app_id, focused)
        yuck = "(box :class 'tasks' :halign 'start' :spacing 15"
        for task in tasks.values():
            yuck += task.make_widget()
        yuck += ")"
        print(yuck, flush=True)
