set -U editor nvim
fish_vi_key_bindings
set fish_greeting

wal -R -q
wal --preview
set PATH $PATH /home/brudihawo/bin/

alias jupyterlab='python -m jupyterlab'
alias feh='feh --auto-zoom --scale-down'

# alias fe='nvim (find -type f | fzf --preview "bat --style=numbers --color=always --line-range=:80 {}" -0)'

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
eval /home/brudihawo/miniconda3/bin/conda "shell.fish" "hook" $argv | source
# <<< conda initialize <<<

