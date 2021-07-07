#!/bin/bash
GRUVBOX_MODE=1

if [ $GRUVBOX_MODE -eq 0 ]; then
  . ~/.cache/wal/colors.sh
else
  background="#282828"
  foreground="#ebdbb2"
  color0="#282828"
  color8="#928374"
  color1="#cc241d"
  color9="#fb4934"
  color2="#98971a"
  color10="#b8bb26"
  color3="#d79921"
  color11="#fabd2f"
  color4="#458588"
  color12="#83a598"
  color5="#b16286"
  color13="#d3869b"
  color6="#689d6a"
  color14="#8ec07c"
  color7="#a89984"
  color15="#ebdbb2"
fi

export color0="$color0"
export color1="$color1"
export color2="$color2"
export color3="$color3"
export color4="$color4"
export color5="$color5"
export color6="$color6"
export color7="$color7"
export color8="$color8"
export color9="$color9"
export color10="$color10"
export color11="$color11"
export color12="$color12"
export color13="$color13"
export color14="$color14"
export color15="$color15"
export background="$background"
export foreground="$foreground"

export EDITOR="$(if [[ -n $DISPLAY ]]; then echo 'termite -e nvim'; else echo 'nvim'; fi)"

nitrogen --restore &
picom &
setxkbmap de &
dunst -config <(envsubst < ~/.config/dunst/dunstrc) &
greenclip daemon &
flameshot &
pacmd set-default-sink alsa_output.hw_2 &
nextcloud --background &
light-locker &
amixer -c 2 sset Speaker 151 &
