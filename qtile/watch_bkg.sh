#/usr/bin/bash

inotifywait -e close_write,moved_to,create -m "$HOME/mypaint/" | 
  while read -r directory events filename; do
    if [ "$filename" = "daily.ora" ]; then
      echo "updating"

      display_cfg=$(autorandr --current 2> /dev/null)

      imgpath="$HOME/mypaint/daily.ora"
      bkgpath="$HOME/mypaint/daily_bkg.png"
      lockpath="$HOME/mypaint/daily_blurred.png"
      python3 $HOME/dotfiles/qtile/set_lockscreen_bkg.py $imgpath $bkgpath $lockpath
    fi
  done
