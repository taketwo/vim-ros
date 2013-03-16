" Vim syntax file
" Language:     rosaction
" Maintainer:   Sergey Alexandrov <alexandrov88@gmail.com>
" Filenames:    *.action

" Read the rosmsg syntax to start with
if version < 600
  so <sfile>:p:h/rosmsg.vim
else
  runtime! syntax/rosmsg.vim
  unlet b:current_syntax
endif

syn match rosactionSeparator   "^---$"

hi def link rosactionSeparator Special

let b:current_syntax = "rosaction"
