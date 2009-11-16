# -*- coding: utf-8 -*-

import codecs
import os
import os.path as p
import pprint
import re
import shutil
import subprocess

from markdoc.builder import Builder
from markdoc.cli.parser import subparsers


def command(function):
    """Decorator to declare a function as a Markdoc CLI task."""
    
    function.parser = subparsers.add_parser(
        function.__name__.replace('_', '-'),
        help=function.__doc__.rstrip('.'))
    return function


## Utilities

@command
def show_config(config, args):
    """Pretty-print the current Markdoc configuration."""
    
    pprint.pprint(config)


## Cleanup

@command
def clean_html(config, args):
    """Clean built HTML from the HTML root."""
    
    if p.exists(config.html_dir):
        shutil.rmtree(config.html_dir)
    os.makedirs(config.html_dir)


@command
def clean_temp(config, args):
    """Clean built HTML from the temporary directory."""
    
    if p.exists(config.temp_dir):
        shutil.rmtree(config.temp_dir)
    os.makedirs(config.temp_dir)


## Synchronization

@command
def sync_static(config, args):
    """Sync static files into the HTML root."""
    
    if not p.exists(config.html_dir):
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


@command
def sync_html(config, args):
    """Sync built HTML and static media into the HTML root."""
    
    if not p.exists(config.html_dir):
        os.makedirs(config.html_dir)
    
    command = 'rsync -vax --delete --ignore-errors --exclude=".*" --exclude="_*"'.split()
    if args.quiet:
        command.append('-q')
    # rsync needs the paths to have trailing slashes to work correctly.
    command.append(p.join(config.temp_dir, ''))
    command.append(p.join(config.static_dir, ''))
    command.append(p.join(config.html_dir, ''))
    
    if not args.quiet:
        print subprocess.list2cmdline(command)
    
    subprocess.check_call(command)


## Building

@command
def build(config, args):
    """Compile wiki to HTML and sync to the HTML root."""
    
    clean_temp(config, args)
    
    builder = Builder(config)
    for rel_filename in builder.walk():
        html = builder.render_document(rel_filename)
        out_filename = p.join(config.temp_dir,
            p.splitext(rel_filename)[0] + p.extsep + 'html')
        
        if not p.exists(p.dirname(out_filename)):
            os.makedirs(p.dirname(out_filename))
        
        fp = codecs.open(out_filename, 'w', encoding='utf-8')
        try:
            fp.write(html)
        finally:
            fp.close()
    
    sync_html(config, args)
    build_listing(config, args)


@command
def build_listing(config, args):
    """Create listings for all directories in the HTML root (post-build)."""
    
    list_basename = config.setdefault('listing-filename', '_list.html')
    builder = Builder(config)
    generate_listing = config.get('generate-listing', 'always').lower()
    always_list = True
    if generate_listing == 'never':
        return # No need to continue.
    
    for fs_dir, _, _ in os.walk(config.html_dir):
        index_file_exists = any([
            p.exists(p.join(fs_dir, 'index.html')),
            p.exists(p.join(fs_dir, 'index'))])
        
        if (generate_listing == 'sometimes') and index_file_exists:
            continue
        
        directory = '/' + '/'.join(p.relpath(fs_dir, start=config.html_dir).split(p.sep))
        if directory == '/' + p.curdir:
            directory = '/'
        
        listing = builder.render_listing(directory)
        list_filename = p.join(fs_dir, list_basename)
        
        fp = codecs.open(list_filename, 'w', encoding='utf-8')
        try:
            fp.write(listing)
        finally:
            fp.close()
        
        if not index_file_exists:
            shutil.copyfile(list_filename, p.join(fs_dir, 'index.html'))

## Serving

IPV4_RE = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')

@command
def serve(config, args):
    """Serve the built HTML from the HTML root."""
    
    # This should be a lazy import, otherwise it'll slow down the whole CLI.
    from markdoc.wsgi import MarkdocWSGIApplication
    
    app = MarkdocWSGIApplication(config)
    
    extra_config = {}
    if args.port:
        extra_config['port'] = args.port
    if args.interface:
        if not IPV4_RE.match(args.interface):
            serve.parser.error('Invalid interface specifier: %r' % args.interface)
        extra_config['bind'] = args.interface
    
    server = config.server_maker(**extra_config)(app)
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

serve.parser.add_argument('-p', '--port', type=int, default=None,
    help="Listen on specified port (default is 8008)")
serve.parser.add_argument('-i', '--interface', default=None,
    help="Bind to specified interface (defaults to loopback only)")
