function fga
  if test (git ls-files -m -o | count) -ne "0"
    set FILES (git ls-files -m -o | fzf --preview 'bat --style=numbers --color=always --line-range=:200 {}' --multi)
    if test (count $FILES) -ne "0" 
      commandline "git add "(echo $FILES | tr '\n' ' ')
    end
  end
end
