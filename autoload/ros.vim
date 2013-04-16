" File: autoload/ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS plugin

" Load guard {{{

if exists('g:autoloaded_ros') || &cp
    finish
endif
let g:autoloaded_ros = '0.0'

if !exists("g:ros_use_python_version")
    let g:_rpy=":py3 "
    if !has("python3")
        if !has("python")
            echo  "ROS Vim requires py >= 2.6 or any py3"
            finish
        endif
        let g:_rpy=":py "
    endif
    let g:ros_use_python_version = "<tab>"
else
    if g:ros_use_python_version == 2
        let g:_rpy=":py "
    else
        let g:_rpy=":py3 "
    endif
endif

" }}}
" Startup code {{{

exec g:_rpy "import sys"
exec g:_rpy "sys.path.append('". g:ros_plugin_path ."')"
exec g:_rpy "import rosvim"

" }}}
" Commands {{{

command! -nargs=0 A exec g:_rpy 'rosvim.alternate()'

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec g:_rpy 'rosvim.buf_enter()'
augroup END

" }}}
