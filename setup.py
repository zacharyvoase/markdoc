# -*- coding: utf-8 -*-

import distutils.core
import os
import re


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


def get_version():
    filename = os.path.join(os.path.dirname(__file__),
        'src', 'markdoc', '__init__.py')
    fp = open(filename)
    try:
        contents = fp.read()
    finally:
        fp.close()
    return re.search(r"__version__ = '([^']+)'", contents).group(1)


def find_packages():
    packages = []
    root = os.path.join(os.path.dirname(__file__), 'src')
    for dirpath, subdirs, filenames in os.walk(root):
        if '__init__.py' in filenames:
            rel = os.path.relpath(dirpath, start=root)
            packages.append(rel.replace(os.path.sep, '.'))
    return packages


def find_package_data():
    files = []
    src_root = os.path.join(os.path.dirname(__file__), 'src', 'markdoc')
    static_root = os.path.join(src_root, 'static')
    for dirpath, subdirs, filenames in os.walk(static_root):
        for filename in filenames:
            if not filename.startswith('.') or filename.startswith('_'):
                abs_path = os.path.join(dirpath, filename)
                files.append(os.path.relpath(abs_path, start=src_root))
    return files


distutils.core.setup(**{
    'name':         'Markdoc',
    'version':      get_version(),
    'author':       'Zachary Voase',
    'author_email': 'zacharyvoase@me.com',
    'url':          'http://bitbucket.org/zacharyvoase/markdoc',
    'description':  'A lightweight Markdown-based wiki build tool.',
    'packages':     find_packages(),
    'package_dir':  {'': 'src'},
    'package_data': {'markdoc': find_package_data()},
    'scripts':      ['bin/markdoc'],
})
