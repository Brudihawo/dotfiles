#!/bin/bash

config=( \
  "nvim"
  "picom"
  "rofi"
  "wal"
  "qtile"
  "Trolltech.conf"
  "dunst"
  "zathura"
  "alacritty"
)
files=( \
  ".Xresources"
  ".bashrc"
  ".zshrc"
  ".tmux.conf"
)

for link in ${config[@]}; do
  echo "Linking $link"
  ln -srf ~/dotfiles/$link ~/.config/
done

for link in ${files[@]}; do
  echo "Linking $link"
  ln -srf ~/dotfiles/$link ~/
done

xrdb ~/.Xresources
