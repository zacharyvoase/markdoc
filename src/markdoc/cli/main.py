# -*- coding: utf-8 -*-

import logging
import os
import argparse

from markdoc.cli import commands
from markdoc.cli.parser import parser
from markdoc.config import Config, ConfigNotFound


def main(cmd_args=None):
    """The main entry point for running the Markdoc CLI."""
    
    if cmd_args is not None:
        args = parser.parse_args(cmd_args)
    else:
        args = parser.parse_args()
    
    if args.command != 'init':
        try:
            args.config = os.path.abspath(args.config)
            
            if os.path.isdir(args.config):
                config = Config.for_directory(args.config)
            elif os.path.isfile(args.config):
                config = Config.for_file(args.config)
            else:
                raise ConfigNotFound("Couldn't locate Markdoc config.")
        except ConfigNotFound, exc:
            parser.error(str(exc))
    else:
        config = None
    
    logging.getLogger('markdoc').setLevel(getattr(logging, args.log_level))
    
    command = getattr(commands, args.command.replace('-', '_'))
    return command(config, args)


if __name__ == '__main__':
    main()
