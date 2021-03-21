#!/usr/bin/bash

home="/home/brudihawo"
xres_file="$home/.Xresources"
theme_file="$home/.config/awesome/themes/wal_theme/theme.lua"
qtile_file="$home/.config/qtile/config.py"
dunst_file="$home/.config/dunst/dunstrc"
termite_file="$home/.config/termite/config"

color_names=( \
  "background"
  "foreground"
  "color0"
  "color8"
  "color1"
  "color9"
  "color2"
  "color10"
  "color3"
  "color11"
  "color4"
  "color12"
  "color5"
  "color13"
  "color6"
  "color14"
  "color7"
  "color15"
)

colors=( \
  "#282828"
  "#ebdbb2"
  "#282828"
  "#928374"
  "#cc241d"
  "#fb4934"
  "#98971a"
  "#b8bb26"
  "#d79921"
  "#fabd2f"
  "#458588"
  "#83a598"
  "#b16286"
  "#d3869b"
  "#689d6a"
  "#8ec07c"
  "#a89984"
  "#ebdbb2"
)

i=0
while [ $i -lt 18 ]; do
  echo "/${color_names[$i]}"': /c\'"${color_names[$i]}: \"${colors[$i]}\""
  sed -i --follow-symlinks "/${color_names[$i]}"'=/c\'"*${color_names[$i]}=\"${colors[$i]}\"" $theme_file
  sed -i --follow-symlinks "/${color_names[$i]}"': /c\'"${color_names[$i]}: \"${colors[$i]}\"" $xres_file
  sed -i --follow-symlinks "/clr_${color_names[$i]}"' = /c\'"clr_${color_names[$i]} = \"${colors[$i]}\"" $qtile_file
  sed -i --follow-symlinks "/clr_${color_names[$i]}"' = /c\'"clr_${color_names[$i]} = \"${colors[$i]}\"" $dunst_file
  sed -i --follow-symlinks "/${color_names[$i]}"' = /c\'"${color_names[$i]} = ${colors[$i]}" $termite_file
  i=$(($i + 1))
done

xrdb $xres_file

