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

exec ':py import sys'
exec ':py sys.path.append("' . g:ros_plugin_path . '")'
exec ':py import rosvim'

" }}}
" Commands {{{

command! -nargs=0 A exec ':py rosvim.alternate()'

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec ':py rosvim.buf_enter()'
augroup END

" }}}
