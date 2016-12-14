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
syn match rosSubArg "\$(arg .\{-})" containedin=xmlString,rosparamTag
syn match rosSubFind "\$(find .\{-})" containedin=xmlString,rosparamTag
syn match rosSubAnon "\$(anon .\{-})" containedin=xmlString,rosparamTag

hi link rosSubArg Macro
hi link rosSubFind Macro
hi link rosSubAnon Macro

" YAML highlighting in <rosparam> tags
syn region rosparamTag
        \ start=#\(<rosparam[^>]\{-}>\)#
        \ end=#\(</rosparam>\)#
        \ fold
        \ contains=xmlTag,xmlEndTag,@YAML
        \ keepend
syn cluster xmlRegionHook add=rosparamTag

let b:current_syntax = "roslaunch"
