#!/bin/bash

source ~/dotfiles/colors.sh
WALLPAPER=$1
LOCK_WALLPAPER=$2

export EDITOR="$(if [[ -n $DISPLAY ]]; then echo 'alacritty -e nvim'; else echo 'nvim'; fi)"

# Screen Timeout
xset s 600

# Background Image and Compositor
picom &
nitrogen --restore &

# Notifications
dunst -config <(envsubst < ~/.config/dunst/dunstrc) &

# Audio
pacmd set-default-sink alsa_output.hw_2 &
amixer -c 2 sset Speaker 151 &

# Clipboard
greenclip daemon &

# Nextcloud
nextcloud --background &

# Redshift and Screen Locker
redshift -l 49:8.4 &
xss-lock -- i3lock -e -i $LOCK_WALLPAPER &

# Wacom Tablet Settings
xsetwacom set "Wacom Intuos BT M Pen stylus" MapToOutput $((2160 * 21600 / 13500))x2160+0+0 &
xsetwacom set "Wacom Intuos BT M Pad pad" Button 1 "key b" &
xsetwacom set "Wacom Intuos BT M Pad pad" Button 2 "key +shift v -shift" &
xsetwacom set "Wacom Intuos BT M Pad pad" Button 3 "key +ctrl z -ctrl" &
xsetwacom set "Wacom Intuos BT M Pad pad" Button 8 "key +ctrl +shift z -shift -ctrl" &
