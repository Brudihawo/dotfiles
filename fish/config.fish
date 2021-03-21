set -U editor nvim
fish_vi_key_bindings
set fish_greeting

# wal -R -q
# wal --preview
set PATH $PATH /home/brudihawo/bin/
set -x MANPAGER 'nvim -c "set ft=man" -'

alias jupyterlab='python -m jupyterlab'
alias feh='feh --auto-zoom --scale-down'
alias env='env | fzf'

alias packlist="pacman -Q | awk '{ printf(\"%-30s %50s\\n\", \$1, \$2) }' | fzf"
alias packup="pacman -Qu | awk '{ printf(\"%-30s %20s %s %s\\n\", \$1, \$2, \$3, \$4) }' | fzf"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
eval /home/brudihawo/miniconda3/bin/conda "shell.fish" "hook" $argv | source
# <<< conda initialize <<<

