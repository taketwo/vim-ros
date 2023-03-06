local M = {}

function M.setup()
  require('cmp').register_source('rosmsg', require('cmp_rosmsg').new())
  require('telescope').load_extension('ros')
end

return M
