# -*- coding: utf-8 -*-

import os

import argparse

from markdoc.config import Config


parser = argparse.ArgumentParser(**{
    'prog': 'markdoc',
    'description': 'A Markdown-based documentation build tool',
    'version': '1.0'
})

config = parser.add_argument('--config', '-c', default=os.getcwd(),
    help="Use the specified Markdoc config (a YAML file or a directory "
         "containing markdoc.yaml)")

subparsers = parser.add_subparsers(dest='command', title='commands', metavar='CMD')

