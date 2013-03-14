" Vim syntax file
" Language:     rosmsg
" Maintainer:   Sergey Alexandrov <alexandrov88@gmail.com>
" Filenames:    *.msg

if exists("b:current_syntax")
  finish
endif

syn keyword rosmsgType      bool
syn keyword rosmsgType      int8
syn keyword rosmsgType      uint8
syn keyword rosmsgType      int16
syn keyword rosmsgType      uint16
syn keyword rosmsgType      int32
syn keyword rosmsgType      uint32
syn keyword rosmsgType      int64
syn keyword rosmsgType      uint64
syn keyword rosmsgType      float32
syn keyword rosmsgType      float64
syn keyword rosmsgType      string
syn keyword rosmsgType      time
syn keyword rosmsgType      duration
syn keyword rosmsgType      Header

syn match rosmsgArray       "\[\d*\]"
syn match rosmsgField       "\s\+\a\w*"

syn match rosmsgComment     "\v#.*$"

hi def link rosmsgType      Type
hi def link rosmsgArray     Statement
hi def link rosmsgField     Identifier
hi def link rosmsgComment   Comment

let b:current_syntax = "rosmsg"
