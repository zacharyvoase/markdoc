# -*- coding: utf-8 -*-

import os.path as p
import shutil
import tempfile

from markdoc.config import Config


def get_temporary_config():
    
    """
    Return a temporary Markdoc configuration.
    
    The contents of the wiki will be copied from the example Markdoc wiki. After
    you're done with this, you should call `clean_temporary_config()` on the
    config object.
    """
    
    own_config_dir = p.join(p.dirname(p.abspath(__file__)), 'example') + p.sep
    temp_config_dir = p.join(tempfile.mkdtemp(), 'example')
    shutil.copytree(own_config_dir, temp_config_dir)
    return Config.for_directory(temp_config_dir)


def clean_temporary_config(config):
    """Delete a temporary configuration's wiki root."""
    
    shutil.rmtree(p.dirname(config['meta.root']))
