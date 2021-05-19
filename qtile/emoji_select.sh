#!/bin/bash
# Select an Emoji from the emoji list and add it to the clipboard

EMOJI_FILE="$HOME/workspace/emoji_select/emojis.txt" 
if [ $1 == '--fzf' ]; then
  cat $EMOJI_FILE | fzf | awk '{printf $1}' | xclip -selection clipboard -i
elif [ $1 == '--rofi' ]; then
  cat $EMOJI_FILE | rofi -dmenu -p "Select Emoji" | awk '{printf $1}' | xclip -selection clipboard -i
fi
