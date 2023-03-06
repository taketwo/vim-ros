local pickers = require('telescope.pickers')
local finders = require('telescope.finders')
local previewers = require('telescope.previewers')
local conf = require('telescope.config').values

local M = {}

function M.msg_picker(opts)
  opts = opts or {}
  pickers
    .new(opts, {
      prompt_title = 'ROS messages',
      finder = finders.new_oneshot_job({ 'rosmsg', 'list' }, opts),
      previewer = previewers.new_buffer_previewer({
        title = 'ROS message preview',
        get_buffer_by_name = function(_, entry) return 'rosmsg/' .. tostring(entry.value) end,
        define_preview = function(self, entry)
          if self.state.bufname then return end
          require('telescope.previewers.utils').job_maker({ 'rosmsg', 'show', entry.value }, self.state.bufnr, {
            bufname = self.state.bufname,
            value = entry.value,
            callback = function(bufnr, _) require('telescope.previewers.utils').regex_highlighter(bufnr, 'rosmsg') end,
          })
          local entries = vim.split(vim.fn.system('rosmsg show ' .. entry.value), '\n')
          vim.api.nvim_buf_set_lines(self.state.bufnr, 0, -1, false, entries)
        end,
      }),
      sorter = conf.generic_sorter(opts),
    })
    :find()
end

return M
