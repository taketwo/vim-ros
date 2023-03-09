local Config = require('vim-ros.config')

local M = {}

---@param opts? RosConfig
function M.setup(opts)
  Config.setup(opts)
  require('cmp').register_source('rosmsg', require('cmp_rosmsg').new())
  require('telescope').load_extension('ros')
end

return M
