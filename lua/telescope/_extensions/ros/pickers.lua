local pickers = require('telescope.pickers')
local finders = require('telescope.finders')
local previewers = require('telescope.previewers')
local conf = require('telescope.config').values

local M = {}

local log = require('vim-ros.logger')
log:warn('vim-ros is being set up')

function M.msg_picker(opts)
  opts = opts or {}
  local messages = vim.fn.py3eval('rosp.list_messages_with_paths()')
  pickers
    .new(opts, {
      prompt_title = 'ROS messages',
      finder = finders.new_table({
        results = messages,
        entry_maker = function(entry)
          return {
            value = entry,
            display = entry[1],
            ordinal = entry[1],
          }
        end,
      }),
      previewer = previewers.new_buffer_previewer({
        title = 'ROS message preview',
        get_buffer_by_name = function(_, entry) return 'rosmsg/' .. tostring(entry.value[1]) end,
        define_preview = function(self, entry)
          conf.buffer_previewer_maker(entry.value[2], self.state.bufnr, {
            bufname = self.state.bufname,
            callback = function(bufnr, _) require('telescope.previewers.utils').regex_highlighter(bufnr, 'rosmsg') end,
          })
        end,
      }),
      sorter = conf.generic_sorter(opts),
    })
    :find()
end

return M
