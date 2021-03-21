function fcp
  set FILES (find -L $argv \( -type f \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
  if test (count $FILES) -ne "0" 
    commandline "cp "(echo $FILES | tr '\n' ' ')
  end
end
