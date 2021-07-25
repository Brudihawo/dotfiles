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
  ['tht'] = '<cmd>Telescope help_tags<cr>',
  ['tgs'] = '<cmd>Telescope grep_string<cr>',
  ['tds'] = '<cmd>Telescope lsp_document_symbols<cr>',
  ['tdd'] = '<cmd>Telescope lsp_document_diagnostics<cr>',
  ['tkm'] = '<cmd>Telescope keymaps<cr>',

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

-- Actually settings the keymaps
set_km("n", n_key_tbl, true, false)
set_km("i", i_key_tbl, true, false)
set_km("x", x_key_tbl, true, false)

return {
  normal = n_key_tbl,
  insert = i_key_tbl,
  ex = x_key_tbl
}
