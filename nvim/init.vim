set runtimepath^=~/dotfiles/vim 
set runtimepath+=~/dotfiles/vim/after
let &packpath=&runtimepath
source ~/dotfiles/vim/.vimrc

lua <<EOF
require'nvim-treesitter.configs'.setup {
  ensure_installed = {"python", "latex", "c", "cpp", "bibtex", "json", "bash"}, -- one of "all", "maintained" (parsers with maintainers), or a list of languages
  ignore_install = { "javascript" }, -- List of parsers to ignore installing
  highlight = {
    enable = true,              -- false will disable the whole extension
    disable = {},  -- list of language that will be disabled
  },
}
EOF
