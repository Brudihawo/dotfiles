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
  if test $(wc -w <<< $FILES) -ne "0"; then
    putcmdline rm -f $(echo $FILES | tr '\n' ' ')
  fi
}

# fuzzy move files
function fmv {
  FILES=$(find -L $* \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) 2> /dev/null | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test $(wc -w <<< $FILES) -ne "0"; then
    putcmdline mv $(echo $FILES | tr '\n' ' ')
  fi
}

# fuzzy git add (only if in git repo directory)
function fga {
  if test $(git ls-files -m -o | wc -w) -ne "0"; then
    FILES=$(git ls-files -m -o | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
    if test $(wc -w <<< $FILES) -ne "0"; then
      putcmdline git add $(echo $FILES | tr '\n' ' ')
    fi
  fi
}

function zathopen {
  FILE=$(find -L "${1:-.}" \( -type f \) -a ! \( -wholename '*.git/*' \) -a ! \( -name '*.git' \) -a \( -wholename '*.pdf' \) | sort | fzf)
  echo "Chose $FILE"
  if test $(wc -w <<< $FILE) -ne "0"; then
    zathura "$FILE"
  fi
}

function pdfwords {
  MIN_CHARS=${2:-7}
  pdftotext $1 - | tr ' ' '\n' |\
    sed -r 's/(http|www).*//g' |\
    sed -r s'/\[.*\]//g' |\
    tr '/' '\n' |\
    sed -r 's/[][„“.?!$%,:;(){}<>"'"'"'=]//g' |\
    sed -r 's/[0-9]+//g' |\
    sed -r "s/^.{1,$(($MIN_CHARS - 1))}\$//g" |\
    sort -u | xargs
}

function repeat {
  while [ : ]; do
    $@
  done
}

function zpushd {
  pushd "$(zoxide query -i)"
}

function nvim_add {
  pushd ~/dotfiles/nvim/pack/editing/start
  git submodule add $1
  popd
}
