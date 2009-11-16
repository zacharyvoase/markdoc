# -*- coding: utf-8 -*-

import os
import os.path as p
import pprint
import subprocess

from markdoc.cli.parser import subparsers


def command(function):
    """Decorator to declare a function as a Markdoc CLI task."""
    
    function.parser = subparsers.add_parser(
        function.__name__.replace('_', '-'),
        help=function.__doc__.rstrip('.'))
    return function


@command
def show_config(config, args):
    """Pretty-print the current Markdoc configuration."""
    
    pprint.pprint(config)


@command
def sync_static(config, args):
    """Synchronize static files into the HTML root."""
    
    os.makedirs(config.html_dir)
    
    command = 'rsync -vax --ignore-errors --exclude=".*" --exclude="_*"'.split()
    if args.quiet:
        command.append('-q')
    # rsync needs the paths to have trailing slashes to work correctly.
    command.append(p.join(config.static_dir, ''))
    command.append(p.join(config.html_dir, ''))
    
    if not args.quiet:
        print subprocess.list2cmdline(command)
    
    subprocess.check_call(command)

sync_static.parser.add_argument('--quiet', '-q',
    action='store_true', default=False,
    help="Suppress non-error output")
