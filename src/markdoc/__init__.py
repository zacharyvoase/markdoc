# -*- coding: utf-8 -*-

import logging
import os
import os.path as p


__version__ = '0.6.1'


static_dir = p.join(p.dirname(__file__), 'static')
default_static_dir = p.join(static_dir, 'default-static')
default_template_dir = p.join(static_dir, 'default-templates')


if not hasattr(p, 'relpath'):
    def relpath(path, start=p.curdir):
        """Return a relative version of a path"""
        
        if not path:
            raise ValueError("no path specified")
        
        start_list = p.abspath(start).split(p.sep)
        path_list = p.abspath(path).split(p.sep)
        
        # Work out how much of the filepath is shared by start and path.
        i = len(p.commonprefix([start_list, path_list]))
        
        rel_list = [p.pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return p.curdir
        return p.join(*rel_list)
    p.relpath = relpath


default_formatter = logging.Formatter(
    u'%(name)s: %(levelname)s: %(message)s')

console_handler = logging.StreamHandler() # By default, outputs to stderr.
console_handler.setFormatter(default_formatter)
console_handler.setLevel(logging.DEBUG)

logging.getLogger('markdoc').addHandler(console_handler)
logging.getLogger('markdoc').setLevel(logging.INFO) # Default level.

# These modules all initialize various default config values, so need to be
# imported straight away.
import markdoc.builder
import markdoc.directories
import markdoc.render
import markdoc.server
import markdoc.templates
