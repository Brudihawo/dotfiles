setopt NO_CASE_GLOB

# History
HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
setopt EXTENDED_HISTORY
setopt SHARE_HISTORY
setopt APPEND_HISTORY
setopt INC_APPEND_HISTORY
setopt HIST_IGNORE_DUPS
setopt HIST_REDUCE_BLANKS

# completion
autoload -Uz compinit && compinit

# colors
autoload -U colors && colors

# Prompt
PROMPT='%K{magenta}%* %k%F{magenta}%f %B%F{red}%n@%m  %f%b'

# vi mode
bindkey -v

# nvim as manpager
export MANPAGER="nvim -c 'set ft=man' -"

# Theme
wal -q -R
wal --preview 
