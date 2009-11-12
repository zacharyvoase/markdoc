# -*- coding: utf-8 -*-

"""
Ensure that configurations are built correctly from markdoc.yaml files.

    >>> import markdoc.config
    >>> config = markdoc.config.Config.for_directory(CONFIG_DIR)
    >>> config['meta']['root'] == CONFIG_DIR
    True

"""

import os


CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'doc')