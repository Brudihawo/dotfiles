function fd
  set DIR (find -L . \( -type d,l \) -a ! \( -wholename "*.git/*" \) -a ! \( -name "*.git" \) | fzf --preview 'tree {}' -q "$argv")
  if test (count $DIR) -ne "0" 
    cd $DIR
  end
end
