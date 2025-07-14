#!/usr/bin/bash

sizes=(
  "S"
  "M"
)
display_cfg=$(autorandr --current 2> /dev/null)

for size in ${sizes[@]}; do
  # Active Pen Region
  if [[ $display_cfg == "home" ]]; then
    xsetwacom set "Wacom Intuos BT $size Pen stylus" MapToOutput 3840x2160+2560+0
  elif [[ $display_cfg == "work" ]]; then
    xsetwacom set "Wacom Intuos BT $size Pen stylus" MapToOutput 2560x1440+2560+0
  else
    xsetwacom set "Wacom Intuos BT $size Pen stylus" MapToOutput 2560x1600+0+0
  fi

  # Pressure Curve
  xsetwacom set "Wacom Intuos BT $size Pen stylus" PressureCurve 0 50 50 100

  # Pen Buttons
  xsetwacom set "Wacom Intuos BT $size Pen stylus" Button 2 "button +1"
  xsetwacom set "Wacom Intuos BT $size Pen stylus" Button 3 "button +2"

  # Pad Buttons
  xsetwacom set "Wacom Intuos BT $size Pad pad" Button 1 "key v"
  xsetwacom set "Wacom Intuos BT $size Pad pad" Button 2 "key b"
  xsetwacom set "Wacom Intuos BT $size Pad pad" Button 3 "key +ctrl z -ctrl"
  xsetwacom set "Wacom Intuos BT $size Pad pad" Button 8 "key +ctrl +shift z -shift -ctrl"
done
