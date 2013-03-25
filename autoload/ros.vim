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

function! ros#BufInit(path)
    let b:ros_package_root = a:path
    let b:ros_package_name = fnamemodify(a:path,':s?\(.*\)[\/]\(.*$\)?\2?')
    call s:BufFiletype()
    return b:ros_package_root
endfunction

function! s:BufFiletype()
    if &filetype =~# '^python\>'
        if exists(':UltiSnipsAddFiletypes')
            UltiSnipsAddFiletypes rospy
        endif
    elseif &filetype =~# '^cpp\>'
        if exists(':UltiSnipsAddFiletypes')
            UltiSnipsAddFiletypes roscpp
        endif
    endif
    if expand('%:e') =~ '^msg$'
        setlocal filetype=rosmsg
        setlocal omnifunc=ros#msg_complete
    elseif expand('%:e') =~ '^srv$'
        setlocal filetype=rossrv
        setlocal omnifunc=ros#msg_complete
    elseif expand('%:e') =~ '^action$'
        setlocal filetype=rosaction
        setlocal omnifunc=ros#msg_complete
    elseif expand('%:e') =~ '^launch$'
        setlocal filetype=roslaunch.xml
        setlocal omnifunc=ros#launch_complete
    elseif expand('%:e') =~ '^cfg$'
        setlocal filetype=python
        if exists(':UltiSnipsAddFiletypes')
            UltiSnipsAddFiletypes roscfg.python
        endif
    elseif expand('%:t') =~ '^manifest.xml$'
        if exists(':UltiSnipsAddFiletypes')
            UltiSnipsAddFiletypes rosmanifest
        endif
    endif
endfunction

" }}}
" Commands {{{

command! -buffer -nargs=0 A exec g:_rpy 'rosvim.alternate()'

" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec g:_rpy 'rosvim.buf_enter()'
augroup END

" }}}
