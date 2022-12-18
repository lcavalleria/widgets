# Generate a yuck string with the contents of hyprland workspaces.
# To be used as deflisten literal in the workspaces widget.
# requires socat

import subprocess
import os

class Workspace:
    def __init__(self, workspace_id, focused=False):
        self.workspace_id = workspace_id
        self.focused = focused

    def make_widget(self):
        if (self.focused == True):
            css_class = "workspacefocused"
        else:
            css_class = "workspace"
        return("(box :class '{css_class}' :width 26 :halign 'center' (label :limit-width 1 :show-truncated false :text '{workspace_id}'))".format(css_class=css_class, workspace_id=self.workspace_id))


workspaces = dict()
his = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]

initialWorkspaceId = subprocess.run(['hyprctl', 'workspaces'], stdout=subprocess.PIPE,universal_newlines=True).stdout.split('\n', 1)[0].split(' ')[2]
workspaces[initialWorkspaceId] = Workspace(initialWorkspaceId)

def renderWorkspace():
        yuck = "(box :class 'workspaces' :halign 'start' :spacing 15"
        sortedWorkspaces = sorted(list(workspaces.items()))
        for id_workspace in sortedWorkspaces:
            yuck += id_workspace[1].make_widget()
        yuck += ")"
        print(yuck, flush=True)

process = subprocess.Popen(["socat", "-", "UNIX-CONNECT:/tmp/hypr/{his}/.socket2.sock".format(his=his)], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in process.stdout:
    if not line: break
    e = line.split(">>")
    event = e[0]
    workspace_id = e[1].strip('\n')
    needs_render = False
    if (event == "workspace"):
        for workspace in workspaces.values(): workspace.focused = False
        workspaces[workspace_id] = Workspace(workspace_id, True)
        needs_render = True
    elif (event == "createworkspace"):
        workspaces[workspace_id] = Workspace(workspace_id)
    elif (event == "destroyworkspace"):
        needs_render = True
        workspaces.pop(workspace_id)
    if (needs_render):
        renderWorkspace()

