# -*- coding: utf-8 -*-

import distutils.core
import os
import re


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


distutils.core.setup(**{
    'name':         'markdoc',
    'version':      get_version(),
    'author':       'Zachary Voase',
    'author_email': 'zacharyvoase@me.com',
    'url':          'http://bitbucket.org/zacharyvoase/markdoc',
    'description':  'A lightweight Markdown-based wiki build tool.',
    'license':      'X11',
    'packages':     find_packages(),
    'package_dir':  {'': 'src'},
    'scripts':      ['bin/markdoc'],
})
