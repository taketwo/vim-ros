This plugin activates itself for files that belong to some ROS package.

Features
========

Sets `&makeprg` to `catkin_make`, `catkin build`, or `rosmake <package-name>` so
that the package, to which the file being edited belongs, could be built with
`:make`.

Editor commands
---------------

- `:A` to alternate between different kinds of C/C++ files (_.cpp_, _.cc_, _.h_, _.hh_, _.hpp_, _.impl_) in the current package
- `:Roscd` to cd to an arbitrary ROS package (with tab-completion)
- `:Rosed`/`:TabRosed`/`:SpRosed`/`:VspRosed` to open arbitrary files (with tab-completion of both
  package and filenames)

Filetype support
----------------

### Message, service, and action files

- syntax highlighting
- omni-completion for message types
- goto message definition with `gd` command

### Launch files

- syntax highlighting (as xml + yaml inside `<rosparam>` tags)
- syntax check (if [Syntastic][] is available)
- omni-completion
  * package names
  * node and nodelet names
  * substitution args
  * environment variables
  * paths with `$(find ...)` substitution
- goto file with `gf` command when the cursor is on a tag
  * with 'file' attribute
  * with an attribute that has a value matching `$(find ...` pattern

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
\   'rosmsg,rossrv,rosaction' : ['re!^', '/'],
\ }
```

UltiSnips
---------

Syntastic
---------

Installation
============

It is recommended to instal `vim-ros` using [vim-plug][]. The (somewhat dated)
alternatives are [Vundle][] or [pathogen][].

This plugin makes use of `rospkg` and (optionally) `catkin-tools` Python
packages. Run the following command in your termanil to make sure that they are
installed (replace `vim` with `nvim` if necessary):

```bash
vim -c "python3 import pip._internal; pip._internal.main(['install', 'rospkg', 'catkin-tools'])" -c "qall"
```

Options
=======

- `g:ros_make` [current|all] Controls which package to build
- `g:ros_catkin_make_options` Additional options for catkin_make (i.e '-j4 -DCMAKE_BUILD_TYPE=Debug' ...)
- `g:ros_disable_warnings` Suppress warnings about lack of Python 3 support and/or inability to import `rospkg`.

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

MIT License. Copyright (c) 2013-2021 Sergey Alexandrov.

[pathogen]: https://github.com/tpope/vim-pathogen
[Vundle]: https://github.com/gmarik/vundle
[vim-plug]: https://github.com/junegunn/vim-plug
[vim-rails]: https://github.com/tpope/vim-rails
[Syntastic]: https://github.com/scrooloose/syntastic
[YouCompleteMe]: https://github.com/Valloric/YouCompleteMe
