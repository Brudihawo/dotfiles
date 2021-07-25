vim.o.runtimepath = '~/dotfiles/vim,' .. vim.o.runtimepath
vim.o.runtimepath = vim.o.runtimepath .. ',~/dotfiles/vim/after'
vim.o.packpath = vim.o.runtimepath

-- Formatting
vim.o.encoding = 'utf-8'
vim.o.tabstop = 2
vim.o.shiftwidth = 2
vim.o.expandtab = true
vim.o.linebreak = true
vim.o.wrap = true

vim.o.backspace = 'indent,eol,start'
vim.o.display = 'lastline'

-- search
vim.o.hlsearch = true
vim.o.smartcase = true

-- highlighting and Readability
vim.o.syntax = 'on'
vim.o.ruler = true
vim.o.showcmd = true
vim.o.autoindent = true
vim.o.cursorline = true
vim.g.indent_guides_enable_on_vim_startup = 1
vim.g.rainbow_active = 1

-- HTML Color code Highlighting
vim.g.Hexokinase_highlighters = { "virtual" }

vim.o.laststatus = 2
vim.o.confirm = true
vim.o.number = true
vim.o.ttimeout = true
vim.o.ttimeoutlen = 200
vim.o.pastetoggle = '<F10>'

-- layout
vim.o.cmdheight = 5
vim.o.laststatus = 2
vim.o.ambiwidth = 'single'

-- Colorscheme
vim.o.termguicolors = true
vim.g.gruvbox_bold = true
vim.g.gruvbox_italic = true
vim.g.gruvbox_underline = true

-- vim.g.gruvbox_improved_strings = true
vim.g.gruvbox_improved_warnings = true

vim.g.gruvbox_italicize_strings = true
vim.g.gruvbox_italicise_comments = true

vim.g.gruvbox_guisp_fallback = 'fg'

vim.g.gruvbox_hls_cursor = true
vim.g.gruvbox_termcolors = 256
vim.g.gruvbox_invert_selection = true

vim.g.colors_name = 'gruvbox'

-- UltiSnips Config
vim.g.UltiSnipsExpandTrigger = "<c-X>"
vim.g.UltiSnipsJumpForwardTrigger = "<c-b>"
vim.g.UltiSnipsJumpBackwardTrigger = "<c-z>"

-- Markdown Preview
vim.g.mkdp_browser = 'firefox'

-- Color Column
vim.o.colorcolumn = "80"

-- Updatetime
vim.o.updatetime = 800

-- VimTeX
vim.g.vimtex_compiler_name = 'nvr'
vim.g.vimtex_compiler_method = 'latexmk'
vim.g.vimtex_view_general_viewer = 'zathura'
vim.g.vimtex_view_method = 'zathura'
vim.g.vimtex_compiler_latexmk_engines = {
  ['_']                = '-lualatex',
  ['pdflatex']         = '-pdf',
  ['dvipdfex']         = '-pdfdvi',
  ['lualatex']         = '-lualatex',
  ['xelatex']          = '-xelatex',
  ['context (pdftex)'] = '-pdf -pdflatex=texexec',
  ['context (luatex)'] = '-pdf -pdflatex=context',
  ['context (xetex)']  = '-pdf -pdflatex=\'\'texexec --xtx\'\'',
}

vim.g.vimtex_compiler_latexmk = {
  ['executable']   = 'latexmk',
  ['callback']     = 1,
  ['hooks']        = {},
  ['options']      = {
     '-file-line-error',
     '-synctex=1',
     '-interaction=nonstopmode',
  },
}


vim.g.vimtex_quickfix_ignore_filters = {
 'Overfull \\hbox',
 'Underfull \\hbox',
}

-- Vim-cmake
vim.g.cmake_generate_options ={ '-G', 'Ninja', '-B', 'build' }

-- Barbar.nvim
vim.g.bufferline = {
  tabpages = true,
  closable = false,
  clickable = false,
}

-- Minimap 
vim.g.minimap_git_colors = true
vim.g.minimap_highlight_search = true

require('my_autocommands')
require('my_keymapping')

-- Extend text objects
surround_pairs = {
  [':'] = ':',
  ['.'] = '.',
  [','] = ',',
  ['/'] = '/',
  ['<bar>'] = '<bar>',
  ['_'] = '_',
  ['-'] = '-',
  ['>'] = '<',
}

for key, value in pairs(surround_pairs) do
  for _, action in ipairs({ "c", "d", "v", "y" }) do
    vim.api.nvim_set_keymap("n", action .. 'i' .. key,
                                 'T' .. key .. action .. 't' .. value,
                                 { noremap = true, silent = false })
    vim.api.nvim_set_keymap("n", action .. 'a' .. key,
                                 'F' .. key .. action .. 'f' .. value,
                                 { noremap = true, silent = false })
  end
end


require'nvim-treesitter.configs'.setup {
  ensure_installed = { "python", "c", "cpp", "bibtex", "json", "bash", "lua", "rust" }, -- one of "all", "maintained" (parsers with maintainers), or a list of languages
  ignore_install = { "javascript" }, -- List of parsers to ignore installing
  highlight = {
    enable = true,              -- false will disable the whole extension
    disable = {},  -- list of language that will be disabled
  },
}

require('hop').setup { keys="asdfghjklöä", term_seq_bias=0.5 }

require('neoscroll').setup {
    -- All these keys will be mapped. Pass an empty table ({}) for no mappings
    mappings = {'<C-u>', '<C-d>', '<C-b>', '<C-f>',
                '<C-y>', '<C-e>', 'zt', 'zz', 'zb'},
    hide_cursor = true,          -- Hide cursor while scrolling
    stop_eof = true,             -- Stop at <EOF> when scrolling downwards
    respect_scrolloff = false,   -- Stop scrolling when the cursor reaches the scrolloff margin of the file
    cursor_scrolls_alone = true  -- The cursor will keep on scrolling even if the window cannot scroll further
}

require('my_telescope_config')
require('my_lsp_config')

require('lualine').setup {
  options= {
    theme = 'gruvbox',
    section_separators = "",
    component_separators = "|",
  },
   sections = {
     lualine_a = {{'mode', lower=false}}, 
     lualine_b = {'branch'},
     lualine_c = {'filename', 'progress', 'diff'},
     lualine_x = {'filetype'}, 
     lualine_y = {'encoding'}, 
     lualine_z = {{'diagnostics', sources={'nvim_lsp'}}}, 
   },
  extensions = {
    'quickfix',
    'fugitive'
  }
}
