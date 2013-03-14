" File: ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS support

" Load guard {{{

if exists('did_ros_vim') || &cp || version < 700
    finish
endif

if !exists("g:RosUsePythonVersion")
    let g:_rpy=":py3 "
    if !has("python3")
        if !has("python")
            echo  "RosVim requires py >= 2.6 or any py3"
            finish
        endif
        let g:_rpy=":py "
    endif
    let g:RosUsePythonVersion = "<tab>"
else
    if g:RosUsePythonVersion == 2
        let g:_rpy=":py "
    else
        let g:_rpy=":py3 "
    endif
endif

" }}}

" Global variables {{{

if !exists("g:RosFoo")
    let g:RosFoo = "Bar"
endif

" }}}

" Global commands {{{

command! -nargs=* RosFooBar :exec g:_rpy "rosvim.foobar("<args>")"

" }}}

" Global functions {{{

function! RosFooBar()
    "exec g:_rpy "rosvim.foobar('" . &ft . "')"
    return ""
endfunction

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

" Startup code {{{

exec g:_rpy "import vim, os, sys"
exec g:_rpy "new_path = vim.eval('expand(\"<sfile>:h\")')"
exec g:_rpy "sys.path.append(new_path)"
exec g:_rpy "import rosvim"

let did_ros_vim=1
