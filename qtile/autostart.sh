#!/bin/bash

source ~/dotfiles/colors.sh
WALLPAPER=$1
LOCK_WALLPAPER=$2

export EDITOR="$(if [[ -n $DISPLAY ]]; then echo 'alacritty -e nvim'; else echo 'nvim'; fi)"

# Clipboard
greenclip daemon &

# Background Image and Compositor
picom &
nitrogen --restore &

# Notifications
dunst -config <(envsubst < ~/.config/dunst/dunstrc) &

# Audio
pacmd set-default-sink alsa_output.hw_2 &
amixer -c 2 sset Speaker 151 &

# Nextcloud
nextcloud --background &

# Redshift and Screen Locker
redshift -l 49:8.4 &
xss-lock -- i3lock -e -i $LOCK_WALLPAPER &

pcmanfm -d &
udiskie &

# Screen Timeout
xset s 600
setxkbmap de -variant nodeadkeys

$HOME/dotfiles/qtile/watch_bkg.sh &
$HOME/dotfiles/qtile/wacom_setup.sh &

eval $(ssh-agent -t 10m) &
