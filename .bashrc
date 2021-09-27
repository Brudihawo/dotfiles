#
# ~/.bashrc
#

[[ $- != *i* ]] && return

colors() {
  local fgc bgc vals seq0

  printf "Color escapes are %s\n" '\e[${value};...;${value}m'
  printf "Values 30..37 are \e[33mforeground colors\e[m\n"
  printf "Values 40..47 are \e[43mbackground colors\e[m\n"
  printf "Value  1 gives a  \e[1mbold-faced look\e[m\n\n"

  # foreground colors
  for fgc in {30..37}; do
    # background colors
    for bgc in {40..47}; do
      fgc=${fgc#37} # white
      bgc=${bgc#40} # black

      vals="${fgc:+$fgc;}${bgc}"
      vals=${vals%%;}

      seq0="${vals:+\e[${vals}m}"
      printf "  %-9s" "${seq0:-(default)}"
      printf " ${seq0}TEXT\e[m"
      printf " \e[${vals:+${vals+$vals;}}1mBOLD\e[m"
    done
    echo; echo
  done
}

[ -r /usr/share/bash-completion/bash_completion ] && . /usr/share/bash-completion/bash_completion

# Change the window title of X terminals
case ${TERM} in
  xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|interix|konsole*|alacritty)
    PROMPT_COMMAND='echo -ne "\033]0;Alacritty - ${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
    ;;
  screen*)
    PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
    ;;
esac

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/hawo/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/hawo/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/hawo/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/hawo/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

check_conda_env ()
{
    if [ ! -z "$CONDA_DEFAULT_ENV" ]; then
      printf -- "%s" " ($CONDA_DEFAULT_ENV)"
    else
      printf -- "%s" ""
    fi
}

modified_path ()
{
    dir=$(sed "s|$HOME|~|g" <<< $(pwd))
    bname=$(basename "$(pwd)")
    dead_len=$((9 + $(wc -m <<< "$(check_conda_env)$HOSTNAME@$USER: ")))
    if [ $(wc -m <<< $dir) -gt $(($(stty -a | awk -F "[; ]" 'FNR == 1 {print $9}') - $dead_len )) ]; then
      outdir=$(awk 'BEGIN { RS="/"; LF} { printf(substr($1, 0, 1)); printf "/" }'  <<< $(sed "s|/$bname||" <<< "$dir"))
      printf "$outdir$bname"
    else
      echo $dir
    fi
}

use_color=true
# Set colorful PS1 only on colorful terminals.
# dircolors --print-database uses its own built-in database
# instead of using /etc/DIR_COLORS.  Try to use the external file
# first to take advantage of user additions.  Use internal bash
# globbing instead of external grep binary.
safe_term=${TERM//[^[:alnum:]]/?}   # sanitize TERM
match_lhs=""
[[ -f ~/.dir_colors   ]] && match_lhs="${match_lhs}$(<~/.dir_colors)"
[[ -f /etc/DIR_COLORS ]] && match_lhs="${match_lhs}$(</etc/DIR_COLORS)"
[[ -z ${match_lhs}    ]] \
  && type -P dircolors >/dev/null \
  && match_lhs=$(dircolors --print-database)
[[ $'\n'${match_lhs} == *$'\n'"TERM "${safe_term}* ]] && use_color=true

if ${use_color} ; then
  title="\e]0;Alacritty - \w\a"
  # Enable colors for ls, etc.  Prefer ~/.dir_colors #64489
  if type -P dircolors >/dev/null ; then
    if [[ -f ~/.dir_colors ]] ; then
      eval $(dircolors -b ~/.dir_colors)
    elif [[ -f /etc/DIR_COLORS ]] ; then
      eval $(dircolors -b /etc/DIR_COLORS)
    fi
  fi

  if [[ ${EUID} == 0 ]] ; then
    PS1='\[\033[01;33m\] ╭─ \[\033[00m\]\A \[\033[01;31m\]\h\[\033[01;36m\]: '"\$(modified_path)"'\[\033[01;31m\]\[\033[01;33m\]\n ╰─❯ \[\033[00m\]'
  else
    PS1='\[\033[01;33m\] ╭─ \[\033[00;35m\]'"\$(check_conda_env)"' \[\033[00m\]\A \[\033[01;34m\]\u\[\033[01;33m\]@\h\[\033[01;37m\]: '"\$(modified_path)"'\[\033[01;32m\]\[\033[00m\]\n\[\033[01;33m\] ╰─❯ \[\033[00m\]'
  fi

  alias ls='ls --color=auto'
  alias grep='grep --colour=auto'
  alias egrep='egrep --colour=auto'
  alias fgrep='fgrep --colour=auto'
else
  if [[ ${EUID} == 0 ]] ; then
    # show root@ when we don't have colors
    PS1=' ╭─ \A \u@\h: \w\n ╰─❯ '
  else
    PS1=' ╭─ \A \u@\h: \w\n ╰─❯ '
  fi
fi

unset use_color safe_term match_lhs sh

alias cp="cp -i"                          # confirm before overwriting something
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias np='nano -w PKGBUILD'
alias more=less

xhost +local:root > /dev/null 2>&1

complete -cf sudo

# Bash won't get SIGWINCH if another process is in the foreground.
# Enable checkwinsize so that bash will check the terminal size when
# it regains control.  #65623
# http://cnswww.cns.cwru.edu/~chet/bash/FAQ (E11)
shopt -s checkwinsize

shopt -s expand_aliases

# export QT_SELECT=4

# Enable history appending instead of overwriting.  #139609
shopt -s histappend

#
# # ex - archive extractor
# # usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

eval "$(zoxide init bash)"

# MY STUFF
export MANPAGER='nvim +Man!'
export PATH="$PATH:~/bin:/home/hawo/.cargo/bin:/opt/rocm/bin/"
export MATLABDIR="/home/hawo/local/MATLAB/"
export EDITOR=nvim

source ~/dotfiles/bash_functions.sh
source /usr/share/fzf/completion.bash
source /usr/share/fzf/key-bindings.bash

set -o vi

# MY ALIASES
alias ls='exa --long --header --sort=name -m'
alias env='env | fzf --multi'
alias gst='git status'
alias gcc='git commit'
alias gpsh='git push'
alias hiwicd='cd ~/workspace/hiwi/mze_files'
alias hiwiin='hiwicd && ./connect.sh'
alias batv='bat --theme=gruvbox-dark'
alias qlog='batv ~/.local/share/qtile/qtile.log'
alias zooml='batv ~/Documents/Semester\ 3/links.txt'
alias webcamview='mpv --profile=low-latency --untimed av://v4l2:/dev/video0 --demuxer-lavf-format=video4linux2 --demuxer-lavf-o-set=input_format=mjpeg'
alias hue='python -m hue_controller.control -b hawos_bridge'
alias u_links='batv ~/Documents/Semester\ 3/links.txt'
alias termdown='termdown -b -f colossal -c 10'
alias glog="git log --pretty='%Cgreen%cs% Cred%an %Creset%s' --graph"

complete -o bashdefault -o default -F _fzf_path_completion zathura
source /usr/share/bash-completion/completions/git


. "$HOME/.cargo/env"
