# -*- coding: utf-8 -*-

import distutils.core
import os


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
    'version':      '0.1',
    'author':       'Zachary Voase',
    'author_email': 'zacharyvoase@me.com',
    'url':          'http://bitbucket.org/zacharyvoase/markdoc',
    'description':  'Markdown-based system for creating documentation and wikis.',
    'license':      'X11',
    'packages':     find_packages(),
    'package_dir':  {'': 'src'},
    'scripts':      ['bin/markdoc'],
})
