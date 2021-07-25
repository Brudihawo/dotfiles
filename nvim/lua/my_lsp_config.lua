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

require("lsp-colors").setup({
  Error = "#cc241d",
  Warning = "#d79921",
  Information = "#b16286",
  Hint = "#689d6a"
})
