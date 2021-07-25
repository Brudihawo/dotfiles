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

-- Setting weird filetypes
vim.api.nvim_command('autocmd BufNewFile,BufRead .xprofile set filetype=xprofile')
vim.api.nvim_command('autocmd BufNewFile,BufRead *.fish set filetype=fish')

vim.api.nvim_command('autocmd BufNewFile,BufRead *.c setlocal commentstring=//\\ %s')
vim.api.nvim_command('autocmd BufNewFile,BufRead *.cpp setlocal commentstring=//\\ %s')
vim.api.nvim_command('autocmd BufNewFile,BufRead *.h setlocal commentstring=//\\ %s')
vim.api.nvim_command('autocmd BufNewFile,BufRead *.hpp setlocal commentstring=//\\ %s')

-- Setting comment strings
vim.api.nvim_command('autocmd FileType python setlocal commentstring=#\\ %s')
vim.api.nvim_command('autocmd FileType c setlocal commentstring=//\\ %s')
vim.api.nvim_command('autocmd FileType cpp setlocal commentstring=//\\ %s')
vim.api.nvim_command('autocmd FileType vim setlocal commentstring=\"\\ %s')
vim.api.nvim_command('autocmd FileType lua setlocal commentstring=--\\ %s')
vim.api.nvim_command('autocmd FileType xprofile setlocal commentstring=#\\ %s')
vim.api.nvim_command('autocmd FileType fish setlocal commentstring=#\\ %s')

-- Filetype specific run commands
vim.api.nvim_command('autocmd FileType python nnoremap <leader>x :!python % <CR>')
vim.api.nvim_command('autocmd FileType sh nnoremap <leader>x :w <CR>:! bash <<< cat %<CR>')
vim.api.nvim_command('autocmd FileType rust nnoremap <leader>x :w <CR>:! cargo run<CR>')

-- Hold Cursor action
vim.api.nvim_command('autocmd CursorHold * :Lspsaga show_cursor_diagnostics')


-- Remappings 
local function set_km(mode, keytbl, nrm, slnt)
  for key, map in pairs(keytbl) do
    vim.api.nvim_set_keymap(mode, key, map, { noremap = nrm, silent = slnt })
  end
end

-- Normal mode Mappings
n_key_tbl = {
-- line highlighting and numbers
  ['<leader>c'] = ':set cursorline!<CR>',
  ['<leader>n'] = ':set relativenumber!<CR>',

-- Buffer management
  ['<C-j>'] = ':BufferNext<CR>',
  ['<C-k>'] = ':BufferPrevious<CR>',
  ['<C-x>'] = ':bdelete<CR>',

-- Diff functionality
  ['<leader>dgj'] = ':diffget //2<CR>',
  ['<leader>dgk'] = ':diffget //3<CR>',

-- Format line breaks for text sections
  ['<A-Enter>'] = 'g$a<Enter><Esc>',

-- Resizing
  ['<A-j>'] = ':resize +3<CR>',
  ['<A-k>'] = ':resize -3<CR>',
  ['<A-h>'] = ':vertical resize -3<CR>',
  ['<A-l>'] = ':vertical resize +3<CR>',

-- Quickfix lists
  ['<C-Q>'] = ':call ToggleQFlist(0)<CR>',
  ['<leader>cn'] = ':cnext<CR>',
  ['<leader>cp'] = ':cprev<CR>',
  ['<leader>ln'] = ':lnext<CR>',
  ['<leader>lp'] = ':lprev<CR>',

-- Vimspector
  ['<leader>vba'] = '<Plug>VimspectorBalloonEval',
  ['<leader>vsr'] = '<Plug>VimspectorReset',

-- Tagbar
  ['<leader>bo'] = ':Tagbar<CR> ', -- Bar open
  ['<leader>st'] = ':TagbarShowTag<CR>', -- " Show tag

-- LSP
  ['gD'] = ':lua vim.lsp.buf.declaration()<cr>',
  ['gd'] = ':lua vim.lsp.buf.definition()<cr>',
  ['<leader>rn'] = ':Lspsaga rename<CR>',

  ['Lf'] = ':lua vim.lsp.buf.formatting()<CR>',
  ['Ldn'] = ':lua vim.lsp.buf.diagnostic.goto_next()<CR>',
  ['Ldp'] = ':lua vim.lsp.buf.diagnostic.goto_prev()<CR>',
  ['Ldl'] = ':lua vim.lsp.diagnostic.set_loclist()<CR>',
  ['Lld'] = ':Lspsaga show_line_diagnostics<CR>',
  ['Lcd'] = ':Lspsaga show_cursor_diagnostics<CR>',
  ['Lsd'] = ':Lspsaga hover_doc<CR>',
  ['Lsh'] = ':lua require(\'lspsaga.signaturehelp\').signature_help()<CR>',
  ['Lpd'] = ':Lspsaga preview_definition<CR>',

-- Fuzzy Finding
  ['<C-p>'] = ':lua require(\'telescope\').extensions.fzf_writer.files()<cr>',
  ['<C-g>'] = ':lua require(\'telescope\').extensions.fzf_writer.staged_grep()<cr>',
  ['<C-b>'] = '<cmd>Telescope buffers<cr> ',
  ['<C-h>'] = '<cmd>Telescope help_tags<cr>',
  ['tgs'] = '<cmd>Telescope grep_string<cr>',
  ['tds'] = '<cmd>Telescope lsp_document_symbols<cr>',
  ['tdd'] = '<cmd>Telescope lsp_document_diagnostics<cr>',

-- Git
  ['gst'] = ':GitGutterSignsToggle<cr>',
  ['gtt'] = ':GitGutterToggle<cr>',
  ['gsh'] = ':GitGutterStageHunk<cr>',
  ['gph'] = ':GitGutterPreviewHunk<cr>',

-- Hop.nvim 
  ['Hl'] = ':HopLine<cr>',
  ['Hc'] = ':HopChar1<cr>',
  ['Hw'] = ':HopWord<cr>',
  ['Hp'] = ':HopPattern<cr>',

-- Buffer Picking (via Barbar)
  ['Hb'] = ':BufferPick<cr>',

-- Toggle Minimap
  ['<leader>mt'] = ':MinimapToggle<CR>',
}

-- Insert mode Mappings
i_key_tbl = {
-- Select first completion suggestion
  ['<A-Enter>'] = '<Down><Enter>',
}

-- Ex mode Mappings
x_key_tbl = {
  ['<leader>vba'] = '<Plug>VimspectorBalloonEval',
  ['<leader>vsr'] = '<Plug>VimspectorReset',
}

set_km("n", n_key_tbl, true, false)
set_km("i", i_key_tbl, true, false)
set_km("x", x_key_tbl, true, false)

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
    vim.api.nvim_set_keymap("n", action .. 'i' .. key, 'T' .. key .. action .. 't' .. value, { noremap = true, silent = false })
    vim.api.nvim_set_keymap("n", action .. 'a' .. key, 'F' .. key .. action .. 'f' .. value, { noremap = true, silent = false })
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

require("lspconfig").pylsp.setup{}

require("lspconfig").rls.setup{}
-- require('lspconfig').rust_analyzer.setup{}

require("lspconfig").texlab.setup{
    cmd = { "texlab" },
    filetypes = { "tex", "bib" },
    settings = {
      texlab = {
        auxDirectory = ".",
        bibtexFormatter = "texlab",
        build = {
          args = { "-lualatex", "-interaction=nonstopmode", "-synctex=1", "%f" },
          executable = "latexmk",
          forwardSearchAfter = false,
          onSave = false
        },
        chktex = {
          onEdit = false,
          onOpenAndSave = false
        },
        diagnosticsDelay = 300,
        formatterLineLength = 80,
        forwardSearch = {
          args = {}
        },
        latexFormatter = "latexindent",
        latexindent = {
          modifyLineBreaks = false
        }
      }
    }
}

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

vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(
    vim.lsp.diagnostic.on_publish_diagnostics, {
        virtual_text = false;
        underline=true;
    }
)

require('compe').setup {
  enabled = true;
  autocomplete = true;
  debug = false;
  min_length = 1;
  preselect = 'enable';
  throttle_time = 80;
  source_timeout = 200;
  incomplete_delay = 400;
  max_abbr_width = 100;
  max_kind_width = 100;
  max_menu_width = 100;
  source = {
    path = true;
    nvim_lsp = true;
    nvim_lua = true;
    ultisnips = true;
    buffer = true;
    calc = true;
  };
  documentation = {
    winhighlight = "NormalFloat:CompeDocumentation,FloatBorder:CompeDocumentationBorder",
    border = { '╭', '─', '╮', '│', '╯', '─', '╰', '│' },
    max_width = math.floor(vim.o.columns * 0.7),
    max_height = math.floor(vim.o.lines * 0.7),
    min_width = math.floor(vim.o.columns * 0.2),
    min_height = math.floor(vim.o.lines * 0.2),
  };
}

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
      minimum_files_characters = 0,
      use_highlighter = false,
    },
    fzf = {
      fuzzy = true,
      override_generic_sorter = true,
      override_file_sorter = true,
      case_mode = "smart_case",
    }
  }
}

require('telescope').load_extension('fzf_writer')

require('telescope').load_extension('ultisnips')

require('hop').setup { keys="asdfghjklöä", term_seq_bias=0.5 }

require('lualine').setup {
  options= {
    theme = 'gruvbox',
    section_separators = "",
    component_separators = "|",
  },
   sections = {
     lualine_a = {{'mode', lower=false}}, 
     lualine_b = {'branch'},
     lualine_c = {'filename', 'progress', 'diff', 'VimtexCountWords'}, 
     lualine_x = {'filetype'}, 
     lualine_y = {'encoding'}, 
     lualine_z = {{'diagnostics', sources={'nvim_lsp'}}}, 
   },
  extensions = {
    'quickfix',
    'fugitive'
  }
}

require("lsp-colors").setup({
  Error = "#cc241d",
  Warning = "#d79921",
  Information = "#b16286",
  Hint = "#689d6a"
})
