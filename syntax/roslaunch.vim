" Vim syntax file
" Language:     roslaunch
" Maintainer:   Sergey Alexandrov <alexandrov88@gmail.com>
" Filenames:    *.launch

" Read YAML syntax rules that will be used to highlight code inside <rosparam>
" tags. Note that we do this before reading XML rules to make sure that YAML
" rules have lower priority (important for the definition of rosparamTag region)
syntax include @YAML syntax/yaml.vim

unlet b:current_syntax

let g:xml_syntax_folding=1
runtime! syntax/xml.vim

" Substitution args
syn match rosSubAnon "\$(anon .\{-})" containedin=xmlString,rosparamTag
syn match rosSubArg "\$(arg .\{-})" containedin=xmlString,rosparamTag
syn match rosSubFind "\$(find .\{-})" containedin=xmlString,rosparamTag
syn match rosSubOptenv "\$(optenv .\{-})" containedin=xmlString,rosparamTag

hi link rosSubAnon Macro
hi link rosSubArg Macro
hi link rosSubFind Macro
hi link rosSubOptenv Macro

" YAML highlighting in <rosparam> tags
syn region rosparamTag
    \ start=#\(<rosparam[^>/]\{-}>\)#
    \ end=#\(</rosparam>\)#
    \ fold
    \ contains=xmlTag,xmlEndTag,xmlAttribute,xmlString,@YAML
    \ keepend
syn cluster xmlRegionHook add=rosparamTag

let b:current_syntax = "roslaunch"
