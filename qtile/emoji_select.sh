#!/bin/bash
# Select an Emoji from the emoji list and add it to the clipboard

mode=${1:-'--fzf'}

EMOJI_FILE="$HOME/workspace/emoji_select/emojis.txt" 

if [ $mode == '--fzf' ]; then
  cat $EMOJI_FILE | fzf | sed "s/ | /|/" | awk -P -F "|" '{print $1}' | xclip -selection clipboard -i
elif [ $mode == '--rofi' ]; then
  cat $EMOJI_FILE | rofi -dmenu -p "Select Emoji" | sed "s/ | /|/" | awk -P -F "|" '{print $1}' | xclip -selection clipboard -i
fi
