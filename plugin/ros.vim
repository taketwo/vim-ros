" File: plugin/ros.vim
" Author: Sergey Alexandrov <alexandrov88@gmail.com>
" Description: ROS package detection and commands

" Load guard {{{

if exists('loaded_ros') || &cp || version < 700 || !has('python')
    finish
endif

python << PYTHON
import vim
try:
    import rospkg
except ImportError:
    vim.command('let s:rospkg_not_found = 1')
PYTHON

if exists('s:rospkg_not_found')
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

" Controls which build system to use
" Valid options:
"   'catkin' : build with catkin_make
"   'rosbuild' : build with rosmake
if !exists('g:ros_build_system')
	let g:ros_build_system = 'catkin'
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
python << PYTHON
package = rospkg.get_package_name(vim.eval('a:filename'))
if package is not None:
    vim.command('call s:BufInit("{0}")'.format(package))
PYTHON
endfunction

function! s:BufInit(package)
    if s:autoload()
        return ros#BufInit(a:package)
    endif
endfunction

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

if g:ros_lowercase_commands
    cabbrev roscd <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'Roscd' : 'roscd')<CR>
    cabbrev rosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'Rosed' : 'rosed')<CR>
    cabbrev tabrosed <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'TabRosed' : 'tabrosed')<CR>
endif

" }}}
