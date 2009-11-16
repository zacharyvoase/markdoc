# -*- coding: utf-8 -*-

import pprint

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
