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

exec ':pyx import sys'
exec ':pyx sys.path.append("' . g:ros_plugin_path . '")'
exec ':pyx import rosvim'

" }}}
" Commands {{{

command! -nargs=0 A exec ':pyx rosvim.alternate()'

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec ':pyx rosvim.buf_enter()'
augroup END

" }}}
