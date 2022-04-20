#!/bin/bash
# Select an Emoji from the emoji list and add it to the clipboard

mode=${1:-'--fzf'}

EMOJI_FILE="$HOME/workspace/emoji_select/emojis.txt" 
line=""
if [ $mode == '--fzf' ]; then
  line="$(cat $EMOJI_FILE | fzf)"
elif [ $mode == '--rofi' ]; then
  line="$(cat $EMOJI_FILE | rofi -dmenu -p "Select Emoji")"
fi

transformed=$(echo "$line" | sed "s/ | /|/g" | awk -P -F "|" '{print $1}' | sed "s/\n//g")
echo $transformed | xclip -selection clipboard -i
