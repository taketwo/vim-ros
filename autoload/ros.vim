" File: autoload/ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS plugin

" Load guard {{{

if exists('g:autoloaded_ros') || &cp
    finish
endif
let g:autoloaded_ros = '0.0'

" }}}
" Startup code {{{

exec g:_rpy "import sys"
exec g:_rpy "sys.path.append(vim.eval('g:ros_plugin_path'))"
exec g:_rpy "import rosvim"

" }}}
" Commands {{{

command! -nargs=0 A exec g:_rpy "rosvim.alternate()"

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec g:_rpy "rosvim.buf_enter()"
augroup END

" }}}
