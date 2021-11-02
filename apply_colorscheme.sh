#!/bin/bash

color_names=(
  "color0"
  "color1"
  "color2"
  "color3"
  "color4"
  "color5"
  "color6"
  "color7"
  "color8"
  "color9"
  "color10"
  "color11"
  "color12"
  "color13"
  "color14"
  "color15"
  "foreground"
  "background"
)

gruvbox_colors=(
  "#282828"  # color0
  "#cc241d"  # color1
  "#98971a"  # color2
  "#d79921"  # color3
  "#458588"  # color4
  "#b16286"  # color5
  "#689d6a"  # color6
  "#a89984"  # color7
  "#928374"  # color8
  "#fb4934"  # color9
  "#b8bb26"  # color10
  "#fabd2f"  # color11
  "#83a598"  # color12
  "#d3869b"  # color13
  "#8ec07c"  # color14
  "#ebdbb2"  # color15
  "#ebdbb2"  # foreground
  "#1d2021"  # background
)

melange_colors=(
  "#2a2520"  # color0
  "#7d2a2f"  # color1
  "#78997a"  # color2
  "#e49b5d"  # color3
  "#697893"  # color4
  "#b380b0"  # color5
  "#86a3a3"  # color6
  "#ece1d7"  # color7
  "#8e733f"  # color8
  "#f17c64"  # color9
  "#78997a"  # color10
  "#ebc06d"  # color11
  "#88b3b2"  # color12
  "#ce9bcb"  # color13
  "#99d59d"  # color14
  "#ece1d7"  # color15
  "#c1a78e"  # foreground
  "#352f2a"  # background
)

THEME=$(echo -e "gruvbox\nmelange" | fzf)

if [[ $THEME == "gruvbox" ]]; then
  colors=("${gruvbox_colors[@]}")
elif [[ $THEME == "melange" ]]; then
  colors=("${melange_colors[@]}")
else
  echo "ERROR; Colorscheme must be 'melange' or 'gruvbox'."
  exit
fi

# Qtile Colorscheme
if [[ $(grep -c "^colors = .*" ~/dotfiles/qtile/config.py) -ne 1 ]]; then
  echo "More than one instance of color array definition in ~/dotfiles/qtile/config.py"
  echo "Aborting..."
  exit
else
  sed -i "s/^colors = .*/colors = ${THEME}_colors/" ~/dotfiles/qtile/config.py
fi

i=0
while [[ i -lt 18 ]]; do
  # colors.sh -> bash color definitions for use in other programs
  sed -i "s/${color_names[$i]}=.*/${color_names[$i]}=\"${colors[$i]}\"/g" ~/dotfiles/colors.sh

  # Xresources
  sed -i "s/${color_names[$i]}: .*/${color_names[$i]}: \"${colors[$i]}\"/g" ~/dotfiles/.Xresources

  # Rofi config
  sed -i "s/rep${color_names[$i]}: .*/rep${color_names[$i]}: ${colors[$i]};/g" ~/dotfiles/rofi/colorscheme.rasi

  # tmux 
  sed -i "s/${color_names[$i]}=.*/${color_names[$i]}=\'${colors[$i]}\'/g" ~/dotfiles/.tmux.conf
  i=$(($i + 1))
done

xrdb ~/.Xresources

cp ~/dotfiles/alacritty/alacritty.yml ~/dotfiles/alacritty/alacritty.yml.old
source ~/dotfiles/colors.sh
cat ~/dotfiles/alacritty/skeleton.yml | envsubst > ~/dotfiles/alacritty/alacritty.yml
qtile cmd-obj -o cmd -f restart

