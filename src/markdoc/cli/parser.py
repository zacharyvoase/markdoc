# -*- coding: utf-8 -*-

import os

import argparse

import markdoc
from markdoc.config import Config


parser = argparse.ArgumentParser(**{
    'prog': 'markdoc',
    'description': 'A lightweight Markdown-based wiki build tool.',
    'version': markdoc.__version__,
})

config = parser.add_argument('--config', '-c', default=os.getcwd(),
    help="Use the specified Markdoc config (a YAML file or a directory "
         "containing markdoc.yaml)")

quiet = parser.add_argument('--quiet', '-q', default=False, action='store_true',
    help="Suppress non-error output")

subparsers = parser.add_subparsers(dest='command', title='commands', metavar='COMMAND')

