#!/bin/bash

source ~/dotfiles/colors.sh

export EDITOR="$(if [[ -n $DISPLAY ]]; then echo 'alacritty -e nvim'; else echo 'nvim'; fi)"

# Screen Timeout
xset s 600

nitrogen --restore &
picom &
dunst -config <(envsubst < ~/.config/dunst/dunstrc) &
pacmd set-default-sink alsa_output.hw_2 &
nextcloud --background &
amixer -c 2 sset Speaker 151 &
greenclip daemon &
flameshot &
redshift -l 49:8.4 &
xss-lock -- i3lock -e -i /usr/share/wallpapers/julia_set_multicolor_lock.png &
