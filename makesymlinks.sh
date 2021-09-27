#!/bin/bash

config=( \
  "awesome"
  "nvim"
  "picom"
  "rofi"
  "wal"
  "fish"
  "qtile"
  "termite"
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
