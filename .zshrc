set -o vi

export PATH="$HOME/.local/bin:/usr/local/cuda-12.8/bin/:$PATH"
export EDITOR="nvim"
export MANPAGER='nvim +Man!'
export LC_ALL="en_US.UTF-8"

eval "$(zoxide init zsh)"
alias gst="git status"
source "$HOME/.cargo/env"

function venv {
  if [ -f ./venv/bin/activate ]; then
    source ./venv/bin/activate  # commented out by conda initialize
  else
    echo "No venv present"
  fi
}

# NNN config
export NNN_FIFO="/tmp/nnn.fifo"
export NNN_PLUG="p:preview-tui"
export SPLIT='v'

alias today="cd ~/notes; ~/workspace/envy/today.py"
alias ls="exa -lah"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias food="$HOME/mensa_plan/main.py"
alias new-pres="cookiecutter ~/Documents/templates/cookiecutter-beamer/"
alias new-torch="cookiecutter ~/Documents/templates/cookiecutter-dl/"

function ssh-fw () {
  port=$1
  remote=$2
  ssh -NL "$port":localhost:"$port" $remote
}

eval `keychain --eval --timeout 3 -q`

# # >>> conda initialize >>>
# # !! Contents within this block are managed by 'conda init' !!
# __conda_setup="$('/home/ws/oy2699/programs/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/home/ws/oy2699/programs/miniconda3/etc/profile.d/conda.sh" ]; then
#         . "/home/ws/oy2699/programs/miniconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/home/ws/oy2699/programs/miniconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# # <<< conda initialize <<<


# bun completions
[ -s "/home/ws/oy2699/.local/share/reflex/bun/_bun" ] && source "/home/ws/oy2699/.local/share/reflex/bun/_bun"

# bun
export BUN_INSTALL="$HOME/.local/share/reflex/bun"
export PATH="$BUN_INSTALL/bin:$PATH"
