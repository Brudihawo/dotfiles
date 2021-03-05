xres_file="/home/brudihawo/.Xresources"
theme_file="/home/brudihawo/.config/awesome/themes/wal_theme/theme.lua"

. /home/brudihawo/.cache/wal/colors.sh

colors=( \
"$color0"
"$color1"
"$color2"
"$color3"
"$color4"
"$color5"
"$color6"
"$color7"
"$color8"
"$color9"
"$color10"
"$color11"
"$color12"
"$color13"
"$color14"
"$color15"
"$background"
"$foreground"
)
color_names=( \
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
"background"
"foreground"
)

i=0
while [ $i -lt 18 ]; do
  echo "/${color_names[$i]}"'=/c\'"${color_names[$i]}=\"${colors[$i]}\""
  sed -i "/${color_names[$i]}"'=/c\'"${color_names[$i]}=\"${colors[$i]}\"" $theme_file
  sed -i "/${color_names[$i]}"'=/c\'"${color_names[$i]}=\"${colors[$i]}\"" $xres_file
  i=$(($i + 1))
done

xrdb $xres_file
echo 'awesome.restart()' | awesome-client
