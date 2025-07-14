#!/bin/bash


# source ~/dotfiles/colors.sh
WALLPAPER=$1
LOCK_WALLPAPER=$2

# python3 $HOME/dotfiles/qtile/set_lockscreen_bkg.py \
#   $HOME/mypaint/daily.ora \
#   $HOME/mypaint/daily_bkg.png \
#   $HOME/mypaint/daily_blurred.png &

blueman-tray &
krb5-auth-dialog &

# Audio
pasystray &
pacmd set-default-sink alsa_output.hw_2 &

# Redshift and Screen Locker
redshift -l 49:8.4 -b 0.8:0.6 &
xss-lock -- i3lock -e -i $LOCK_WALLPAPER &

pcmanfm -d &

# Screen Timeout
xset s 600

nm-applet &

$HOME/dotfiles/qtile/watch_bkg.sh &
$HOME/dotfiles/qtile/wacom_setup.sh &

eval $(ssh-agent -t 10m) &
