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

exec g:_rpy "import vim, os, sys"
exec g:_rpy "new_path = vim.eval('expand(\"<sfile>:h\")')"
exec g:_rpy "sys.path.append(new_path)"
exec g:_rpy "import rosvim"

function! ros#BufInit(path)
  let b:ros_package_root = a:path
  let b:ros_package_name = fnamemodify(a:path,':s?\(.*\)[\/]\(.*$\)?\2?')
  call s:BufFiletype()
  call s:BufSettings()
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
    setlocal omnifunc=ros#CompleteMsg
  elseif expand('%:e') =~ '^srv$'
    setlocal filetype=rossrv
    setlocal omnifunc=ros#CompleteMsg
  elseif expand('%:e') =~ '^action$'
    setlocal filetype=rosaction
    setlocal omnifunc=ros#CompleteMsg
  elseif expand('%:e') =~ '^launch$'
    setlocal filetype=roslaunch.xml
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

function! s:BufSettings()
  let &makeprg = 'rosmake ' . b:ros_package_name
endfunction

" }}}
" Autocommands {{{

augroup rosPluginAuto
  autocmd!
  autocmd User BufEnterRos call s:BufSettings()
augroup END

" }}}
" Completion commands {{{

function! ros#CompleteMsg(findstart, base)
    if a:findstart
        return 0
    else
        let res = []
        let builtin = [ "bool", "int8", "uint8", "int16", "uint16", "int32",
                      \ "uint32", "int64", "uint64", "float32", "float64",
                      \ "string", "time", "duration", "Header" ]
        for m in builtin + split(system('rosmsg list'), "\n")
            if m =~# '^' . a:base
                call add(res, m)
            endif
        endfor
        return res
    endif
endfun

" }}}
