# -*- coding: utf-8 -*-

"""
    >>> from markdoc.builder import Builder
    >>> b = Builder(CONFIG)

Make sure breadcrumbs are generated properly:

    >>> b.crumbs(CONFIG_DIR + 'wiki/index.md')
    [('index', None)]
    
    >>> b.crumbs(CONFIG_DIR + 'wiki/somefile.md')
    [('somefile', None)]
    
    >>> b.crumbs(CONFIG_DIR + 'wiki/somedir/index.md')
    [('index', '/'), ('somedir', None)]
    
    >>> b.crumbs(CONFIG_DIR + 'wiki/somedir/something.md')
    [('index', '/'), ('somedir', '/somedir/'), ('something', None)]

"""

import os

from markdoc.config import Config


CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'doc') + os.path.sep
CONFIG = Config.for_directory(CONFIG_DIR)
