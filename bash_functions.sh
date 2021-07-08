#!/usr/bin/bash

# put something on the command line as if it was user input
function putcmdline {
  bind '"\e[0n": "'"$*\""; printf '\e[5n'
}

# fuzzy find files for editing
function fe {
  FILES=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) 2> /dev/null | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test $(wc -w <<< $FILES) -ne "0"; then
    nvim $FILES
  fi
}
# fuzzy change directory
function fd {
  DIR=$(find -L $* \( -type d,l \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) 2> /dev/null | fzf --preview 'tree {}')
  if test $(wc -w <<< $DIR) -ne "1";then
    cd $DIR
  fi
}

# fuzzy copy
function fcp {
  FILES=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \)  2> /dev/null | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test $(wc -w <<< $FILES) -ne "0"; then 
    putcmdline cp $(echo $FILES | tr '\n' ' ')
  fi
}

# fuzzy remove files
function frm {
  FILES=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) 2> /dev/null | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test $(wc -w <<< $FILES) -ne "0";then
    putcmdline rm -f $(echo $FILES | tr '\n' ' ')
  fi
}

# fuzzy move files
function fmv {
  FILES=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) 2> /dev/null | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test $(wc -w <<< $FILES) -ne "0";then
    putcmdline mv $(echo $FILES | tr '\n' ' ')
  fi
}

# fuzzy git add (only if in git repo directory)
function fga {
  if test $(git ls-files -m -o | wc -w) -ne "0";then
    FILES=$(git ls-files -m -o | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
    if test $(wc -w <<< $FILES) -ne "0";then 
      putcmdline git add $(echo $FILES | tr '\n' ' ')
    fi
  fi
}

function zathopen {
  FILE=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) -a \( -wholename "*.pdf" \) 2> /dev/null | sort | fzf)
  if test $(wc -w <<< $FILE) -ne "0"; then 
    zathura $FILE
  fi
}

