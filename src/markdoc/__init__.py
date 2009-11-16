# -*- coding: utf-8 -*-

import os


__version__ = '0.1'
static_dir = os.path.join(os.path.dirname(__file__), 'static')
default_static_dir = os.path.join(static_dir, 'default-static')
default_template_dir = os.path.join(static_dir, 'default-templates')


if not hasattr(os.path, 'relpath'):
    def relpath(path, start=os.path.curdir):
        """Return a relative version of a path"""
        
        if not path:
            raise ValueError("no path specified")
        
        start_list = os.path.abspath(start).split(os.path.sep)
        path_list = os.path.abspath(path).split(os.path.sep)
        
        # Work out how much of the filepath is shared by start and path.
        i = len(os.path.commonprefix([start_list, path_list]))
        
        rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return os.path.curdir
        return os.path.join(*rel_list)
    os.path.relpath = relpath
