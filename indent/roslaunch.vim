
" Use XML indentation rules

if exists("b:did_indent")
  finish
endif

" load the XML indent rules
runtime! indent/xml.vim
"runtime! indent/yaml.vim

let b:did_indent = 1

" override the vim indent expression (we'll call it ourselves)
setlocal indentexpr=GetRoslaunchIndent()

" Only define the function once.
if exists("*GetRoslaunchIndent")
  finish
endif

" roslaunch-indent will return yaml indent inside a <rosparam> block, and
" return -1 if not inside a block to trigger auto-indent
function GetRoslaunchIndent()
  if searchpair('<rosparam.\{-}>','','<\/rosparam>','bWnm') > 0
    echo "yaml indenting: ".string(v:lnum)
    "return GetYAMLIndent()
    return -1
  else
    echo "xml indenting: ".string(v:lnum)
    return XmlIndentGet(v:lnum,1)
  endif
endfunc


