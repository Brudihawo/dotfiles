#!/usr/bin/bash

pixels_wacom=$((2160 * 21600 / 13500))
# Active Pen Region
xsetwacom set "Wacom Intuos BT M Pen stylus" MapToOutput ${pixels_wacom}x2160+$((3840 - $pixels_wacom))+0

# Pressure Curve
xsetwacom set "Wacom Intuos BT M Pen stylus" PressureCurve 0 50 50 100

# Pen Buttons
xsetwacom set "Wacom Intuos BT M Pen stylus" Button 2 "key shift"
xsetwacom set "Wacom Intuos BT M Pen stylus" Button 3 "button +2"

# Pad Buttons
xsetwacom set "Wacom Intuos BT M Pad pad" Button 1 "key +alt minus -alt"
xsetwacom set "Wacom Intuos BT M Pad pad" Button 2 "key +shift v -shift"
xsetwacom set "Wacom Intuos BT M Pad pad" Button 3 "key +ctrl z -ctrl"
xsetwacom set "Wacom Intuos BT M Pad pad" Button 8 "key +ctrl +shift z -shift -ctrl"
