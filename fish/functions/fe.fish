function fe
  set FILES (find -L . \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi -q "$argv")
  if test (count $FILES) -ne "0" 
    nvim $FILES
  end
end
