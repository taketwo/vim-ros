"""
Integration with UltiSnips plugin (https://github.com/SirVer/ultisnips).
"""

import vim
import vimp


def is_available():
    """
    Test whether UltiSnips plugin is available (was loaded).
    """
    for v in ['g:did_UltiSnips_plugin', 'g:did_plugin_ultisnips']:
        if v in vimp.var:
            return True
    return False


def add_filetypes(filetypes):
    if isinstance(filetypes, str):
        ft = filetypes
    elif isinstance(filetypes, list):
        ft = '.'.join(filetypes)
    vim.command('UltiSnipsAddFiletypes ' + ft)
