#!/bin/bash

filename="/home/hawo/dotfiles/qtile/keychords_mangled.txt"

cat $filename | yad --list \
  --close-on-unfocus \
  --grid-lines=vertical \
  --no-header \
  --no-click \
  --no-selection \
  --center --width=3000 --height=1688 \
  --title="KEY COMBINATIONS AND KEYS" \
  --column="KEYS":text \
  --column="KEYS (2)":text \
  --column="KEY CHORDS":text

