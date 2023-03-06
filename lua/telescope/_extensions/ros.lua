local pickers = require('telescope._extensions.ros.pickers')

return require('telescope').register_extension({
  exports = {
    msg = pickers.msg_picker,
  },
})
