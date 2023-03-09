local M = {}

---@class RosConfig
M.defaults = {
  ---@type string Format string for vim.notify messages
  notify_format = '[vim-ros] %s',
  ---@type string Logging level (off, error, warn, info, debug, trace)
  log_level = 'warn',
}

---@class RosConfig
M.options = {}

---@param opts? RosConfig
function M.setup(opts) M.options = vim.tbl_deep_extend('force', M.defaults, opts or {}) end

return M
