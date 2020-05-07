" File: plugin/ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS package detection and commands

" Load guard {{{

if exists('g:loaded_ros') || &cp || version < 700
    finish
endif

let g:loaded_ros = 1
let g:ros_plugin_path = escape(expand('<sfile>:p:h'), '\')

" }}}
" Utility functions {{{

function! s:warning(str)
    if !exists('g:ros_disable_warnings')
        echohl WarningMsg
        echomsg a:str
        echohl None
        let v:errmsg = a:str
    endif
endfunction

" }}}
" Python/rospkg check {{{

function! s:ImportRospkg()
    unlet! s:rospkg_not_found
    exec g:_rpy "import vim"
    exec g:_rpy "try: import rospkg\nexcept ImportError: vim.command('let s:rospkg_not_found = 1')"
    return !exists("s:rospkg_not_found")
endfunction

if has("python")
    let g:_rpy=":py "
    if !s:ImportRospkg()
        call s:warning("Disabling vim-ros: unable to import rospkg with Python 2")
        finish
    endif
elseif has("python3")
    let g:_rpy=":py3 "
    if !s:ImportRospkg()
        call s:warning("Disabling vim-ros: unable to import rospkg with Python 3")
        finish
    endif
else
    call s:warning("Disabling vim-ros: Vim with +python or +python3 is required")
    finish
endif

" }}}
" Global variables {{{

" Controls which package(s) to build with :make command
" Valid options:
"   'current' : build the current buffer's package
"   'all'     : build all packages that were opened in this session
if !exists('g:ros_make')
    let g:ros_make = 'all'
endif

" Controls which build system to use
" Valid options:
"   'catkin' : build with catkin_make
"   'rosbuild' : build with rosmake
"   'catkin-tools': build with 'catkin build'
if !exists('g:ros_build_system')
    let g:ros_build_system = 'catkin'
endif

if !exists('g:ros_catkin_make_options')
    let g:ros_catkin_make_options = ''
endif

" Custom commands have to start with a capital letter in Vim. This means that
" you will have to type 'Roscd' or 'Rosed' instead of 'roscd' or 'rosed' that
" your hands are so familiar with. It is possible to have abbreviations for
" commands though. This option will enable creation of command abbreviations
" that make all the 'ros...' commands lowercase.
if !exists('g:ros_lowercase_commands')
    let g:ros_lowercase_commands = 1
endif

" Create custom syntax checker for roslaunch files if Syntastic is available.
if !exists('g:ros_syntastic_integration')
    let g:ros_syntastic_integration = 1
endif

" }}}
" Detection {{{

function! s:Detect(filename)
    exec g:_rpy "package = rospkg.get_package_name(vim.eval('a:filename'))"
    exec g:_rpy "if package: vim.command('call s:BufInit(\"{0}\")'.format(package))"
endfunction

function! s:BufInit(package)
    if s:autoload()
        return ros#BufInit(a:package)
    endif
endfunction

function! s:autoload(...)
    if !exists("g:autoloaded_ros")
        runtime! autoload/ros.vim
    endif
    if exists("g:autoloaded_ros")
        if a:0
            exe a:1
        endif
        return 1
    endif
    call s:warning("Disabling vim-ros: autoload/ros.vim is missing")
    return ""
endfunction

" }}}
" Autocommands {{{

augroup rosPluginDetect
    autocmd!
    autocmd BufNewFile,BufRead * call s:Detect(expand("<afile>:p"))
    autocmd VimEnter * if expand("<amatch>") == "" && !exists("b:ros_package_path") | call s:Detect(getcwd()) | endif | if exists("b:ros_package_path") | silent doau User BufEnterRos | endif
    autocmd FileType netrw if !exists("b:ros_package_path") | call s:Detect(expand("%:p")) | endif | if exists("b:ros_package_path") | silent doau User BufEnterRos | endif
    autocmd BufEnter * if exists("b:ros_package_path") | silent doau User BufEnterRos | endif
    autocmd BufLeave * if exists("b:ros_package_path") | silent doau User BufLeaveRos | endif
    autocmd BufDelete * if exists("b:ros_package_path") | silent doau User BufDeleteRos | endif
augroup END

" }}}
" Commands {{{

command! -nargs=1 -complete=custom,ros#RoscdComplete Roscd :call ros#Roscd(<f-args>)
command! -nargs=* -complete=custom,ros#RosedComplete Rosed :call ros#Rosed(<f-args>)
command! -nargs=* -complete=custom,ros#RosedComplete TabRosed :call ros#TabRosed(<f-args>)
command! -nargs=* -complete=custom,ros#RosedComplete SpRosed :call ros#SpRosed(<f-args>)
command! -nargs=* -complete=custom,ros#RosedComplete VspRosed :call ros#VspRosed(<f-args>)

if g:ros_lowercase_commands
    cabbrev roscd <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'Roscd' : 'roscd')<CR>
    cabbrev rosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'Rosed' : 'rosed')<CR>
    cabbrev tabrosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'TabRosed' : 'tabrosed')<CR>
    cabbrev sprosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'SpRosed' : 'sprosed')<CR>
    cabbrev vsprosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'VspRosed' : 'vsprosed')<CR>
endif

" }}}
