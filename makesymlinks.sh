links=( \
  ".Xresources" \
  ".bashrc"
  ".zshrc"
  "awesome"
  "nvim"
  "picom"
  "rofi"
  "vim"
)


for link in ${links[@]}; do
  echo "Linking $link"
  ln -srf ~/dotfiles/$link ~/.config/

done
