# -*- coding: utf-8 -*-

import os

import argparse

import markdoc
from markdoc.config import Config


parser = argparse.ArgumentParser(**{
    'prog': 'markdoc',
    'description': 'A lightweight Markdown-based wiki build tool.',
})

parser.add_argument('-v', '--version', action='version',
    version=markdoc.__version__)

config = parser.add_argument('--config', '-c', default=os.getcwd(),
    help="Use the specified Markdoc config (a YAML file or a directory "
         "containing markdoc.yaml)")

log_level = parser.add_argument('--log-level', '-l', metavar='LEVEL',
    default='INFO', choices='DEBUG INFO WARN ERROR'.split(),
    help="Choose a log level from DEBUG, INFO (default), WARN or ERROR")

quiet = parser.add_argument('--quiet', '-q',
    action='store_const', dest='log_level', const='ERROR',
    help="Alias for --log-level ERROR")

verbose = parser.add_argument('--verbose',
    action='store_const', dest='log_level', const='DEBUG',
    help="Alias for --log-level DEBUG")

subparsers = parser.add_subparsers(dest='command', title='commands', metavar='COMMAND')
