links=( \
  ".Xresources" \
  ".bashrc"
  ".zshrc"
  "awesome"
  "nvim"
  "picom"
  "rofi"
  "vim"
  "wal"
)


for link in ${links[@]}; do
  echo "Linking $link"
  ln -srf ~/dotfiles/$link ~/.config/

done
