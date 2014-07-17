"""
Integration with YouCompleteMe plugin (https://github.com/Valloric/YouCompleteMe).
"""

import vimp


def is_available():
    """
    Test whether YouCompleteMe plugin is available (was loaded).
    """
    return 'g:loaded_youcompleteme' in vimp.var
