config=( \
  "awesome"
  "nvim"
  "picom"
  "rofi"
  "vim"
  "wal"
)
files=( \
  ".Xresources" 
  ".bashrc"
  ".zshrc"
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
