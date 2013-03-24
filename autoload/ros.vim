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
        setlocal omnifunc=ros#MsgComplete
    elseif expand('%:e') =~ '^srv$'
        setlocal filetype=rossrv
        setlocal omnifunc=ros#MsgComplete
    elseif expand('%:e') =~ '^action$'
        setlocal filetype=rosaction
        setlocal omnifunc=ros#MsgComplete
    elseif expand('%:e') =~ '^launch$'
        setlocal filetype=roslaunch.xml
        setlocal omnifunc=ros#LaunchComplete
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
" Alternate {{{

command! -buffer -nargs=0 A exec g:_rpy 'rosvim.alternate()'

" }}}
" Roscd {{{
" Only implementation, command was already created in plugin/ros.vim

function! ros#Roscd(...)
    exec g:_rpy "rosvim.roscd()"
endfunction

function! ros#RoscdComplete(...)
    exec g:_rpy "rosvim.roscd_complete()"
    return l:result
endfunction

" }}}
" Rosed {{{
" Only implementation, command was already created in plugin/ros.vim

function! ros#Rosed(...)
    exec g:_rpy "rosvim.rosed()"
endfunction

function! ros#RosedComplete(...)
    exec g:_rpy "rosvim.rosed_complete()"
    return l:result
endfunction

" }}}
" }}}
" Autocommands {{{

augroup rosPluginAuto
    autocmd!
    autocmd User BufEnterRos exec g:_rpy 'rosvim.buf_enter()'
augroup END

" }}}
" Completion commands {{{

function! ros#MsgComplete(...)
    exec g:_rpy "rosvim.msg_complete()"
    return l:result
endfun

function! ros#LaunchComplete(...)
    exec g:_rpy "rosvim.launch_complete()"
    return l:result
endfun

" }}}
