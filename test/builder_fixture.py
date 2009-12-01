# -*- coding: utf-8 -*-

import os.path as p

from common import get_temporary_config, clean_temporary_config


def setup_test(test):
    test.globs['CONFIG'] = get_temporary_config()
    test.globs['WIKI_ROOT'] = p.join(test.globs['CONFIG']['meta.root'], '')


def teardown_test(test):
    clean_temporary_config(test.globs['CONFIG'])
