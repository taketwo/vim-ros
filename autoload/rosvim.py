#!/usr/bin/env python
# encoding: utf-8


import vim
import vimp


packages = list()


def buf_enter():
    p = vimp.b['ros_package_name']
    if not p in packages:
        packages.append(p)
    if vimp.g['ros_make'] == 'all':
        cmd = 'set makeprg=rosmake\ ' + '\ '.join(packages)
    else:
        cmd = 'set makeprg=rosmake\ ' + p
    vim.command(cmd)
