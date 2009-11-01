# -*- coding: utf-8 -*-

import distutils.core


distutils.core.setup(**{
    'name':         'markdoc',
    'version':      '0.1',
    'author':       'Zachary Voase',
    'author_email': 'zacharyvoase@me.com',
    'url':          'http://bitbucket.org/zacharyvoase/markdoc',
    'description':  'Markdown-based system for creating documentation and wikis.',
    'license':      'X11',
    'packages':     ['markdoc'],
    'package_dir':  {'markdoc': 'src/markdoc'},
})
