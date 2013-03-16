This plugin activates itself only for files within a (rosbuild-style) ROS
package.

Features
--------

* Adds minimal support for `.msg`, `.srv`, and `.action` files:
  - filetype detection
  - syntax highlighting
  - omni-completion for message types
* Sets `&makeprg` to `rosmake <package-name>` so that the package, to which the
  file being edited belongs, could be built with `:make`.

Installation
------------

I recommend installing `vim-ros` using [pathogen][] or [Vundle][].

Acknowledgments
---------------

The code for package detection is adapted from [vim-rails][] plugin.

[pathogen]: https://github.com/tpope/vim-pathogen
[Vundle]: https://github.com/gmarik/vundle
[vim-rails]: https://github.com/tpope/vim-rails
