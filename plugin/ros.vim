" File: plugin/ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS package detection and commands

" Load guard {{{

if exists('loaded_ros') || &cp || version < 700
    finish
endif
let g:loaded_ros = 1
let g:ros_plugin_path = escape(expand('<sfile>:p:h'), '\')

" }}}
" Global variables {{{

" Controls which package(s) to build with :make command
" Valid options:
"   'current' : build the current buffer's package
"   'all'     : build all packages that were opened in this session
if !exists('g:ros_make')
    let g:ros_make = 'all'
endif

" }}}
" Utility functions {{{

function! s:error(str)
  echohl ErrorMsg
  echomsg a:str
  echohl None
  let v:errmsg = a:str
endfunction

function! s:autoload(...)
  if !exists("g:autoloaded_ros") && v:version >= 700
    runtime! autoload/ros.vim
  endif
  if exists("g:autoloaded_ros")
    if a:0
      exe a:1
    endif
    return 1
  endif
  if !exists("g:ros_no_autoload_warning")
    let g:ros_no_autoload_warning = 1
    if v:version >= 700
      call s:error("Disabling ros.vim: autoload/ros.vim is missing")
    else
      call s:error("Disabling ros.vim: Vim version 7 or higher required")
    endif
  endif
  return ""
endfunction

function! s:escvar(r)
  let r = fnamemodify(a:r, ':~')
  let r = substitute(r, '\W', '\="_".char2nr(submatch(0))."_"', 'g')
  let r = substitute(r, '^\d', '_&', '')
  return r
endfunction

" }}}
" Detection {{{

function! s:Detect(filename)
  if exists('b:ros_package_root')
    return s:BufInit(b:ros_package_root)
  endif
  let fn = substitute(fnamemodify(a:filename, ":p"), '\c^file://', '', '')
  let sep = matchstr(fn, '^[^\\/]\{3,\}\zs[\\/]')
  if sep != ""
    let fn = getcwd().sep.fn
  endif
  if fn =~ '[\/]manifest\.xml$'
    return s:BufInit(strpart(fn, 0, strlen(fn) - 13))
  endif
  if isdirectory(fn)
    let fn = fnamemodify(fn, ':s?[\/]$??')
  else
    let fn = fnamemodify(fn, ':s?\(.*\)[\/][^\/]*$?\1?')
  endif
  let ofn = ""
  let nfn = fn
  while nfn != ofn && nfn != ""
    if exists("s:_".s:escvar(nfn))
      return s:BufInit(nfn)
    endif
    let ofn = nfn
    let nfn = fnamemodify(nfn, ':h')
  endwhile
  let ofn = ""
  while fn != ofn
    if filereadable(fn . "/manifest.xml")
      return s:BufInit(fn)
    endif
    let ofn = fn
    let fn = fnamemodify(ofn,':s?\(.*\)[\/]\(msg\|msg_gen\|srv\|srv_gen\|cfg\|launch\|include\|src\|test\|scripts\|action\)\($\|[\/].*$\)?\1?')
  endwhile
  return 0
endfunction

function! s:BufInit(path)
  let s:_{s:escvar(a:path)} = 1
  if s:autoload()
    return ros#BufInit(a:path)
  endif
endfunction

" }}}
" Initialization {{{

augroup rosPluginDetect
  autocmd!
  autocmd BufNewFile,BufRead * call s:Detect(expand("<afile>:p"))
  autocmd VimEnter * if expand("<amatch>") == "" && !exists("b:ros_package_root") | call s:Detect(getcwd()) | endif | if exists("b:ros_package_root") | silent doau User BufEnterRos | endif
  autocmd FileType netrw if !exists("b:ros_package_root") | call s:Detect(expand("%:p")) | endif | if exists("b:ros_package_root") | silent doau User BufEnterRos | endif
  autocmd BufEnter * if exists("b:ros_package_root") | silent doau User BufEnterRos | endif
  autocmd BufLeave * if exists("b:ros_package_root") | silent doau User BufLeaveRos | endif
  autocmd BufDelete * if exists("b:ros_package_root") | silent doau User BufDeleteRos | endif
augroup END

" }}}
" Commands {{{

command! -nargs=* -complete=custom,ros#RosedComplete Rosed :call ros#Rosed(<f-args>)

" }}}
