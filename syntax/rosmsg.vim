" Vim syntax file
" Language:     rosmsg
" Maintainer:   Sergey Alexandrov <alexandrov88@gmail.com>
" Filenames:    *.msg

if exists("b:current_syntax")
  finish
endif

syn keyword rosmsgBuiltInType      bool
syn keyword rosmsgBuiltInType      int8
syn keyword rosmsgBuiltInType      uint8
syn keyword rosmsgBuiltInType      int16
syn keyword rosmsgBuiltInType      uint16
syn keyword rosmsgBuiltInType      int32
syn keyword rosmsgBuiltInType      uint32
syn keyword rosmsgBuiltInType      int64
syn keyword rosmsgBuiltInType      uint64
syn keyword rosmsgBuiltInType      float32
syn keyword rosmsgBuiltInType      float64
syn keyword rosmsgBuiltInType      string
syn keyword rosmsgBuiltInType      time
syn keyword rosmsgBuiltInType      duration
syn keyword rosmsgBuiltInType      Header

syn match   rosmsgType             "\v^\h\w+(/\h\w+)=" nextgroup=rosmsgArray,rosmsgField,rosmsgConstant
syn match   rosmsgArray            "\[\d*\]"
syn match   rosmsgField            "\v\s+\h\w*(\w*\s*\=)@!"
syn match   rosmsgConstant         "\v\s+\u[0-9A-Z_]*(\s*\=)@="
syn match   rosmsgComment          "\v#.*$"

hi def link rosmsgBuiltInType      Keyword
hi def link rosmsgType             Type
hi def link rosmsgArray            Normal
hi def link rosmsgField            Identifier
hi def link rosmsgConstant         Constant
hi def link rosmsgComment          Comment

let b:current_syntax = "rosmsg"
