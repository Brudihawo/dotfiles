setopt NO_CASE_GLOB

# completion
autoload -Uz compinit && compinit

# colors
autoload -U colors && colors

if [[ $TERM == "linux" ]]; then
  top_chars="┌─"
  top_pad="n"
  bottom_chars="└─>"

  source ~/dotfiles/colors.sh
  echo -ne "\e]P0$color0"
  echo -ne "\e]P1$color1"
  echo -ne "\e]P2$color2"
  echo -ne "\e]P3$color3"
  echo -ne "\e]P4$color4"
  echo -ne "\e]P5$color5"
  echo -ne "\e]P6$color6"
  echo -ne "\e]P7$color7"
  echo -ne "\e]P8$color8"
  echo -ne "\e]P9$color9"
  echo -ne "\e]PA$color10"
  echo -ne "\e]PB$color11"
  echo -ne "\e]PC$color12"
  echo -ne "\e]PD$color13"
  echo -ne "\e]PE$color14"
  echo -ne "\e]PF$color15"
else
  top_chars="╭─"
  top_pad="─"
  bottom_chars="╰─❯"
fi

# Prompt
# PROMPT='%K{magenta}%* %k%F{magenta}%f %B%F{red}%n@%m  %f%b'
PROMPT='%F{green}%*%f %B%F{blue}%n%f%F{yellow}@%m%b%f %~ | '

# completion
zstyle ':completion:*' completer _extensions _complete _approximate
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path "$HOME/.cache/zsh/.zcompcache"
zstyle ':completion:*' menu select
zstyle ':completion:*:*:*:*:descriptions' format '%F{green}-- %d --%f'
zstyle ':completion:*:*:*:*:corrections' format '%F{yellow}-- %d (errors: %e) --%f'
zstyle ':completion:*:warnings' format '%F{purple}-- %d --%f'
zstyle ':completion:*:messages' format '%F{red}-- no matches --%f'

export PATH="$HOME/.cargo/bin:/opt/arduino-cli/bin:/opt/arduino-language-server/bin:$HOME/.local/bin:$PATH"


# vi mode
bindkey -v

# nvim as manpager
export MANPAGER='nvim +Man!'
export EDITOR='nvim'
alias ls='exa -lah'
alias gst='git status'
alias startFoam="bash --init-file ~/.foambashrc"
source /usr/share/fzf/key-bindings.zsh

eval "$(zoxide init zsh)"

venv() {
  if [ -d "./venv" ]; then
    source ./venv/bin/activate
  else
    echo "No venv present. Creating"
    virtualenv venv
  fi
}

# opam configuration
[[ ! -r /home/hawo/.opam/opam-init/init.zsh ]] || source /home/hawo/.opam/opam-init/init.zsh  > /dev/null 2> /dev/null

HISTFILE="$HOME/.zsh_history"
SAVEHIST=10000
setopt share_history
