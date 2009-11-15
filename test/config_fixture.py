# -*- coding: utf-8 -*-

import os.path as p


def setup_test(test):
    test.globs['WIKI_ROOT'] = p.join(p.dirname(p.abspath(__file__)), 'example')
