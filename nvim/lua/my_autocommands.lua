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
