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

if has('python')
    exec ':python import sys'
    exec ':python sys.path.append("' . g:ros_plugin_path . '")'
    exec ':python import rosvim'
else
    exec ':python3 import sys'
    exec ':python3 sys.path.append("' . g:ros_plugin_path . '")'
    exec ':python3 import rosvim'
endif

" }}}
" Commands {{{

if has('python')
    command! -nargs=0 A exec ':python rosvim.alternate()'
else
    command! -nargs=0 A exec ':python3 rosvim.alternate()'
endif

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    if has('python')
	autocmd User BufEnterRos exec ':python rosvim.buf_enter()'
    else
	autocmd User BufEnterRos exec ':python3 rosvim.buf_enter()'
    endif
augroup END

" }}}
