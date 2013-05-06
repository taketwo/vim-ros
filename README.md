This plugin activates itself only for files within a (rosbuild-style) ROS
package.

Features
========

* Sets `&makeprg` to `rosmake <package-name>` so that the package, to which the
  file being edited belongs, could be built with `:make`.
* Adds commands:
  - `:A` to alternate between _.cpp_ and _.h_ files in the current package
  - `:Roscd` to cd to an arbitrary ROS package (with tab-completion)
  - `:Rosed` to open arbitrary files (with tab-completion of both package and
    filenames)

Message, service, and action files
----------------------------------

Adds minimal support for `.msg`, `.srv`, and `.action` files:
  - filetype detection
  - syntax highlighting
  - omni-completion for message types
  - goto message definition with 'gd' command

Launch files
------------

Adds minimal support for `.launch` files:
  - filetype detection
  - syntax highlighting (xml)
  - syntax check (if [Syntastic][] is available)
  - omni-completion for package types
  - goto file with 'gf' command (when the cursor is on a tag with 'filename'
    attribute)

Installation
============

I recommend installing `vim-ros` using [pathogen][] or [Vundle][].

Acknowledgments
===============

Inspired by the [vim-rails][] plugin.

[pathogen]: https://github.com/tpope/vim-pathogen
[Vundle]: https://github.com/gmarik/vundle
[vim-rails]: https://github.com/tpope/vim-rails
[Syntastic]: https://github.com/scrooloose/syntastic
