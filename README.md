This plugin activates itself for files that belong to some ROS package.

Features
========

Sets `&makeprg` to `catkin_make` or `rosmake <package-name>` so that the
package, to which the file being edited belongs, could be built with `:make`.

Editor commands
---------------

- `:A` to alternate between _.cpp_ / _.cc_ and _.h_ / _.hh_ files in the current
  package
- `:Roscd` to cd to an arbitrary ROS package (with tab-completion)
- `:Rosed`/`:TabRosed` to open arbitrary files (with tab-completion of both
  package and filenames)

Filetype support
----------------

### Message, service, and action files

- syntax highlighting
- omni-completion for message types
- goto message definition with `gd` command

### Launch files

- syntax highlighting (as xml)
- syntax check (if [Syntastic][] is available)
- omni-completion
  * package names
  * node names
  * substitution args
  * environment variables
  * paths with `$(find ...)` substitution
- goto file with `gf` command (when the cursor is on a tag with 'filename'
  attribute)

### Xacro files

- syntax highlighting (as xml)
- goto file with `gf` command (when the cursor is on a tag with 'filename'
  attribute)

### Dynamic reconfigure files

- syntax highlighting (as python)

Intergration with other plugins
===============================

`vim-ros` integrates with several other plugins out of the box. This section
lists the plugins and explains suggested configuration.

YouCompleteMe
-------------

> [YouCompleteMe][] is is a fast, as-you-type, fuzzy-search code completion
> engine for Vim.

`vim-ros` provides semantic completion for ROS filetypes via omni-complete
functions. YouCompleteMe will automatically use them, however if you want the
completion to be magically triggered as you type, you have to associate proper
triggers with ROS filetypes in your `.vimrc`:

```viml
let g:ycm_semantic_triggers = {
\   'roslaunch' : ['="', '$(', '/'],
\   'rosmsg,rossrv,rosaction' : ['re!^'],
\ }
```

UltiSnips
---------

Syntastic
---------

Installation
============

It is recommended to instal `vim-ros` using [Vundle][] or [pathogen][].

Contributing
============

The plugin is written in Python and includes a shim to make interfacing with Vim
as easy as it could possibly be. Therefore, extending the plugin does not
require knowledge of the peculiarities of Vim Script. Contributions are welcome!

Acknowledgments
===============

Inspired by the [vim-rails][] plugin.

License
=======

MIT License. Copyright (c) 2013-2014 Sergey Alexandrov.

[pathogen]: https://github.com/tpope/vim-pathogen
[Vundle]: https://github.com/gmarik/vundle
[vim-rails]: https://github.com/tpope/vim-rails
[Syntastic]: https://github.com/scrooloose/syntastic
[YouCompleteMe]: https://github.com/Valloric/YouCompleteMe
