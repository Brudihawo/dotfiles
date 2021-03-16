function fd
  set DIR (find -L $argv \( -type d,l \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) | fzf --preview 'tree {}')
  if test (count $DIR) -ne "0" 
    cd $DIR
  end
end
