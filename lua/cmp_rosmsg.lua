local cmp = require("cmp")
local Job = require("plenary.job")

local source = {}

source.new = function()
  local self = setmetatable({ cache = {} }, { __index = source })
  return self
end

source.complete = function(self, _, callback)
  local bufnr = vim.api.nvim_get_current_buf()
  if not self.cache[bufnr] then
    Job
      :new({
        command = "rosmsg",
        args = { "list" },
        on_exit = function(job)
          local items = {}
          for _, msg in ipairs(job:result()) do
            table.insert(items, {
              label = msg,
              kind = cmp.lsp.CompletionItemKind.Struct,
              documentation = {},
            })
          end
          callback { items = items, isIncomplete = false }
          self.cache[bufnr] = items
        end,
      })
      :start()
  else
    callback { items = self.cache[bufnr], isIncomplete = false }
  end
end

source.get_debug_name = function()
  return "ROS message types"
end

source.is_available = function()
  return vim.bo.filetype == "rosmsg" or vim.bo.filetype == "rossrv" or vim.bo.filetype == "rosaction"
end

return source
