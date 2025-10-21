#!/bin/python3
# Generate a yuck string with the contents of hyprland workspaces.
# To be used as deflisten literal in the workspaces widget.
# requires socat

import os
import subprocess


class Workspace:
    def __init__(self, workspace_id, focused=False):
        self.workspace_id = workspace_id
        self.focused = focused

    def make_widget(self):
        if self.focused is True:
            css_class = "workspacefocused"
        else:
            css_class = "workspace"
        if self.workspace_id == 11:
            self.workspace_id = 1
        return (
            "(box "
            ":class '{css_class}' :width 38 :height 25 :halign 'center' :valign 'center' "
            "(label :limit-width 1 :show-truncated false :text '{workspace_id}')"
            ")"
        ).format(css_class=css_class, workspace_id=str(self.workspace_id - 1))


workspaces = dict()
xrd = os.environ["XDG_RUNTIME_DIR"]
his = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]


def applyWorkspace(workspace_id):
    workspace_id = int(workspace_id) + 1
    workspaces[workspace_id] = Workspace(workspace_id, True)


def renderWorkspace():
    yuck = "(box :class 'workspaces' :halign 'start' :valign 'center' :spacing 10"
    sortedWorkspaces = sorted(list(workspaces.items()))
    for id_workspace in sortedWorkspaces:
        yuck += id_workspace[1].make_widget()
    yuck += ")"
    print(yuck, flush=True)


initialWorkspaceId = (
    subprocess.run(
        ["hyprctl", "workspaces"], stdout=subprocess.PIPE, universal_newlines=True
    )
    .stdout.split("\n", 1)[0]
    .split(" ")[2]
)
applyWorkspace(initialWorkspaceId)


process = subprocess.Popen(
    ["socat", "-", f"UNIX-CONNECT:{xrd}/hypr/{his}/.socket2.sock"],
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

if process.stdout is not None:
    for line in process.stdout:
        print("line:")
        print(line)
        if not line:
            break
        e = line.split(">>")
        print(e)
        event = e[0]
        needs_render = False
        if event == "focusedmon":
            workspace_id = e[1].strip("\n").split(",")[1]
        else:
            workspace_id = e[1].strip("\n")
        if event == "workspace" or event == "focusedmon":
            for workspace in workspaces.values():
                workspace.focused = False
            applyWorkspace(workspace_id)
            needs_render = True
        elif event == "createworkspace":
            applyWorkspace(workspace_id)
        elif event == "destroyworkspace":
            needs_render = True
            workspaces.pop(int(workspace_id) + 1)
        if needs_render:
            renderWorkspace()
