set runtimepath^=~/dotfiles/vim 
set runtimepath+=~/dotfiles/vim/after
let &packpath=&runtimepath
" source ~/dotfiles/vim/.vimrc

lua <<EOF
require'nvim-treesitter.configs'.setup {
  ensure_installed = {"python", "latex", "c", "cpp", "bibtex", "json", "bash", "lua"}, -- one of "all", "maintained" (parsers with maintainers), or a list of languages
  ignore_install = { "javascript" }, -- List of parsers to ignore installing
  highlight = {
    enable = true,              -- false will disable the whole extension
    disable = {},  -- list of language that will be disabled
  },
}
-- require("lspconfig").pylsp.setup{}

require("lspconfig").ccls.setup{
  init_options = {
    index = {
      threads = 0;
    };
    cache = {
      directory = "/tmp/ccls";
    };
  };
  filetypes = { "c", "cc", "cpp", "c++", "objc", "objcpp", "h", "hpp" };
}
require("lspconfig").cmake.setup{}

require('neoscroll').setup({
    -- All these keys will be mapped. Pass an empty table ({}) for no mappings
    mappings = {'<C-u>', '<C-d>', '<C-b>', '<C-f>',
                '<C-y>', '<C-e>', 'zt', 'zz', 'zb'},
    hide_cursor = true,          -- Hide cursor while scrolling
    stop_eof = true,             -- Stop at <EOF> when scrolling downwards
    respect_scrolloff = false,   -- Stop scrolling when the cursor reaches the scrolloff margin of the file
    cursor_scrolls_alone = true  -- The cursor will keep on scrolling even if the window cannot scroll further
})

require('telescope').setup{
  defaults = {
    vimgrep_arguments = {
      'rg',
      '--hidden',
      '--color=never',
      '--no-heading',
      '--with-filename',
      '--line-number',
      '--column',
      '--smart-case'
    },
    prompt_position = "bottom",
    prompt_prefix = "> ",
    selection_caret = "> ",
    entry_prefix = "  ",
    initial_mode = "insert",
    selection_strategy = "reset",
    sorting_strategy = "descending",
    layout_strategy = "horizontal",
    layout_defaults = {
      horizontal = {
        mirror = false,
      },
      vertical = {
        mirror = false,
      },
    },
    file_sorter =  require'telescope.sorters'.get_fuzzy_file,
    file_ignore_patterns = {},
    generic_sorter =  require'telescope.sorters'.get_generic_fuzzy_sorter,
    shorten_path = true,
    winblend = 0,
    width = 0.75,
    preview_cutoff = 120,
    results_height = 1,
    results_width = 0.8,
    border = {},
    borderchars = { '─', '│', '─', '│', '╭', '╮', '╯', '╰' },
    color_devicons = true,
    use_less = true,
    set_env = { ['COLORTERM'] = 'truecolor' }, -- default = nil,
    file_previewer = require'telescope.previewers'.vim_buffer_cat.new,
    grep_previewer = require'telescope.previewers'.vim_buffer_vimgrep.new,
    qflist_previewer = require'telescope.previewers'.vim_buffer_qflist.new,

    -- Developer configurations: Not meant for general override
    buffer_previewer_maker = require'telescope.previewers'.buffer_previewer_maker
  },
  extensions = {
    fzf_writer = {
      minimum_grep_characters = 2,
      minimum_files_characters = 2,
      use_highlighter = true,
    }
  }
}

require('telescope').load_extension('coc')
EOF

set nocompatible

" Formatting set encoding=utf-8
set tabstop=2
set shiftwidth=2
set expandtab
set backspace=indent,eol,start
set display+=lastline
set linebreak
set wrap

" NERDTree Settings
let g:NERDTreeDirArrowExpandable="+"
let g:NERDTreeDirArrowCollapsible="~"
let g:NERDTreeDirArrows=">"

" search
set hlsearch
set ignorecase

" highlighting and Readability
syntax on
set ruler
set showcmd
set autoindent
set cursorline
let g:indent_guides_enable_on_vim_startup=1
let g:rainbow_active=1

" HTML Color code Highlighting
let g:Hexokinase_highlighters=["virtual"]

set nostartofline
set laststatus=2
set confirm
set number relativenumber
set notimeout ttimeout ttimeoutlen=200
set pastetoggle=<F10>
set noshowmode

" layout
set cmdheight=5
set laststatus=2
set ambiwidth=single

" airline colors and colorscheme
set termguicolors
let g:gruvbox_bold = 1
let g:gruvbox_transparent_bg = 0.5
" let g:gruvbox_hls_cursor = 1
let g:gruvbox_italicize_strings = 1
let g:gruvbox_italic = 1
let g:gruvbox_termcolors = 1
let g:gruvbox_invert_selection = 1
colorscheme gruvbox

let g:airline_theme='gruvbox'
let g:airline#extensions#tabline#enabled=1
let g:airline#extensions#tabline#formatter="unique_tail_improved"
let g:airline#extensions#tabline#show_splits=0
let g:airline#extensions#tabline#show_buffers=1
let g:airline_powerline_fonts=1
let g:airline#extensions#branch#enabled=1
let g:airline#extensions#denite#enabled=1
let g:airline#extensions#vimtex#enabled=1
let g:airline#extensions#vimcmake#enabled=1
let g:airline#extensions#whitespace#enabled=1
let g:airline_skip_empty_sections=1
let g:airline#extensions#whitespace#trailing_format='trailing[%s]'

if !exists('g:airline_symbols')
  let g:airline_symbols={}
endif
let g:airline_symbols.maxlinenr = ' col'
let g:airline_symbols.branch = ''
" let g:airline_right_alt_sep = " "
let g:airline_right_alt_sep = "|"
" let g:airline_left_alt_sep = ""
let g:airline_left_alt_sep = "|"
" let g:airline_right_sep = ""
let g:airline_right_sep = ""
let g:airline_left_sep = ""

" Setting weird filetypes
autocmd BufNewFile,BufRead .xprofile set filetype=xprofile
autocmd BufNewFile,BufRead *.fish set filetype=fish

autocmd BufNewFile,BufRead *.c setlocal commentstring=//\ %s
autocmd BufNewFile,BufRead *.cpp setlocal commentstring=//\ %s
autocmd BufNewFile,BufRead *.h setlocal commentstring=//\ %s
autocmd BufNewFile,BufRead *.hpp setlocal commentstring=//\ %s


" Setting comment strings
autocmd FileType python setlocal commentstring=#\ %s
autocmd FileType c setlocal commentstring=//\ %s
autocmd FileType cpp setlocal commentstring=//\ %s
autocmd FileType vim setlocal commentstring=\"\ %s
autocmd FileType lua setlocal commentstring=--\ %s
autocmd FileType xprofile setlocal commentstring=#\ %s
autocmd FileType fish setlocal commentstring=#\ %s

" Remappings nnoremap <C-N> :NERDTreeToggle<CR>
nnoremap <A-C> :colorscheme default<CR>
nnoremap <leader>c :set cursorline!<CR>
nnoremap <leader>n :set relativenumber!<CR>
nnoremap <C-j> :bnext<CR>
nnoremap <C-k> :bprev<CR>
nnoremap <C-x> :bdelete<CR>
nnoremap <leader>dgj :diffget //2<CR>
nnoremap <leader>dgk :diffget //3<CR>


" Resizing
nnoremap <A-j> :resize +3<CR>
nnoremap <A-k> :resize -3<CR>
nnoremap <A-h> :vertical resize -3<CR>
nnoremap <A-l> :vertical resize +3<CR>

" Extending text objects
let pairs = { ':' : ':',
            \ '.' : '.',
            \ ',' : ',',
            \ '/' : '/',
            \ '<bar>' : '<bar>',
            \ '_' : '_',
            \ '-' : '-',
            \ '>' : '<',
            \ }

for [key, value] in items(pairs)
  exec "nnoremap ci".key." T".key."ct".value
  exec "nnoremap ca".key." F".key."cf".value

  exec "nnoremap di".key." T".key."dt".value
  exec "nnoremap da".key." F".key."df".value

  exec "nnoremap vi".key." T".key."vt".value
  exec "nnoremap va".key." F".key."vf".value

  exec "nnoremap yi".key." T".key."yt".value
  exec "nnoremap ya".key." F".key."yf".value
endfor

" Filetype specific run commands
autocmd FileType python nnoremap <leader>x :!python % <CR>
autocmd FileType tex nnoremap <leader>x :w <CR>:! pdflatex -interaction nonstopmode % <CR>
autocmd FileType sh nnoremap <leader>x :w <CR>:! bash <<< cat %<CR>
autocmd FileType rust nnoremap <leader>x :w <CR>:! cargo run<CR>

" UltiSnips Config
let g:UltiSnipsExpandTrigger="<c-Space>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" Quickfix lists
nnoremap <C-Q>:call ToggleQFlist(0)<CR>
nnoremap <leader>cn :cnext<CR>
nnoremap <leader>cp :cprev<CR>
nnoremap <leader>ln :lnext<CR>
nnoremap <leader>lp :lprev<CR>

" Vimspector
let g:vimspector_enable_mappings = 'HUMAN'
" F5	          When debugging, continue. Otherwise start debugging.
" F3	          Stop debugging.
" F4	          Restart debugging with the same configuration.
" F6	          Pause debuggee.
" F9	          Toggle line breakpoint on the current line.
" <leader>F9	  Toggle conditional line breakpoint on the current line.
" F8	          Add a function breakpoint for the expression under cursor
" <leader>F8	  Run to Cursor
" F10	          Step Over
" F11	          Step Into
" F12	          Step out of current function scope

nmap <leader>vba <Plug>VimspectorBalloonEval
xmap <leader>vba <Plug>VimspectorBalloonEval
nmap <leader>vsr <Plug>VimspectorReset
xmap <leader>vsr <Plug>VimspectorReset

" Markdown Preview
let g:mkdp_browser = 'firefox'

" Color Column
set colorcolumn=80,100

" Tagbar
" Bar open
nnoremap <leader>bo :Tagbar<CR> 
" Show tag
nnoremap <leader>st :TagbarShowTag<CR>

" VimTeX
let g:vimtex_compiler_name = 'nvr'

" Vim-cmake
let g:cmake_generate_options=['-G', 'Ninja', '-B', 'build']

" Coc.nvim
function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  elseif (coc#rpc#ready())
    call CocActionAsync('doHover')
  else
    execute '!' . &keywordprg . " " . expand('<cword>')
  endif
endfunction

nnoremap <silent> <leader>rn :call CocActionAsync('rename')<CR>
nnoremap <silent> <leader>cd :call <SID>show_documentation()<CR>
nnoremap <silent> gd :call CocAction('jumpDefinition')<CR>
autocmd CursorHold * silent call CocActionAsync('highlight')

nnoremap cd :CocDiagnostics<CR>
nnoremap cn :CocNext<CR>
nnoremap cp :CocPrev<CR>


" Coc-Telescope / Fuzzy Finding
nnoremap <C-p> <cmd>Telescope find_files find_command=rg,--ignore,--files<cr>
nnoremap <C-g> <cmd>Telescope live_grep find_command=rg,--ignore,--files<cr>
nnoremap <C-b> <cmd>Telescope buffers<cr> 
nnoremap <C-h> <cmd>Telescope help_tags<cr>
nnoremap td <cmd>Telescope coc workspace_diagnostics<cr>
nnoremap ts <cmd>Telescope coc workspace_symbols<cr>
nnoremap tds <cmd>Telescope coc document_symbols<cr>
nnoremap tr <cmd>Telescope coc references<cr>
nnoremap tgs <cmd>Telescope grep_string<cr>

" Git
nnoremap gst :GitGutterSignsToggle<cr>
nnoremap gtt :GitGutterToggle<cr>
nnoremap gsh :GitGutterStageHunk<cr>
nnoremap gph :GitGutterPreviewHunk<cr>
