#!/bin/bash

CURRENT=$(hyprctl devices -j | jq -r '.keyboards[0].layout')

if [[ "$CURRENT" == "us" ]]; then
    hyprctl keyword input:kb_layout es
    hyprctl keyword input:kb_model pc105
else
    hyprctl keyword input:kb_layout us
    hyprctl keyword input:kb_model pc104
fi

# this is kind of dirty
eww update current_locale=$(hyprctl devices -j | jq -r '.keyboards[0].layout')
