" Vim syntax file
" Language: roslaunch XML
" Maintainer: Jonathan Bohren
" Latest Revision: 8 July 2013
"
" roslaunch xml syntax hilighting with inline yaml support
"
" Put the following in your .vimrc:
"   autocmd BufRead,BufNewFile *.launch setfiletype roslaunch

if exists("b:current_syntax")
  finish
endif

let g:xml_syntax_folding=1
runtime! syntax/xml.vim

" roslaunch substitution args
syn match rosSubArg "\$(arg .\{-})" containedin=xmlString
syn match rosSubFind "\$(find .\{-})" containedin=xmlString
syn match rosSubAnon "\$(anon .\{-})" containedin=xmlString

hi link rosSubArg Macro
hi link rosSubFind Macro
hi link rosSubAnon Macro

" handle rosparam yaml hilighting
let s:current_syntax=b:current_syntax
unlet b:current_syntax

syntax include @YAML syntax/yaml.vim
syntax region ymlSnipInline matchgroup=rosparamTag start="\m<.\{-}rosparam.\{-}>" end="\m</.\{-}rosparam.\{-}>" contains=@YAML containedin=xmlRegion
hi link rosparamTag Statement

syn match rosSubArg "\$(arg .\{-})" containedin=ymlSnipInline
syn match rosSubFind "\$(find .\{-})" containedin=ymlSnipInline
syn match rosSubAnon "\$(anon .\{-})" containedin=ymlSnipInline

syn match rosSubAnon "\$(anon .\{-})" containedin=ymlSnipInline

hi link rosSubArg Macro
hi link rosSubFind Macro
hi link rosSubAnon Macro

let b:current_syntax=s:current_syntax


