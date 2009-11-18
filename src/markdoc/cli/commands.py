# -*- coding: utf-8 -*-

import codecs
from functools import wraps
import logging
import os
import os.path as p
import pprint
import re
import shutil
import subprocess

import markdoc
from markdoc.builder import Builder
from markdoc.cli.parser import subparsers


def command(function):
    """Decorator/wrapper to declare a function as a Markdoc CLI task."""
    
    cmd_name = function.__name__.replace('_', '-')
    help = (function.__doc__ or '').rstrip('.') or None
    parser = subparsers.add_parser(cmd_name, help=help)
    
    @wraps(function)
    def wrapper(config, args):
        if not args.quiet:
            print '--> markdoc', cmd_name
        return function(config, args)
    wrapper.parser = parser
    
    return wrapper


## Utilities

@command
def show_config(config, args):
    """Pretty-print the current Markdoc configuration."""
    
    pprint.pprint(config)


@command
def init(_, args):
    """Initialize a new Markdoc repository."""
    
    log = logging.getLogger('markdoc.init')
    
    if not args.destination:
        log.info('No destination specified; using current directory')
        destination = os.getcwd()
    else:
        destination = p.abspath(args.destination)
    
    if os.path.exists(destination) and os.listdir(destination):
        init.parser.error("destination isn't empty")
    elif not os.path.exists(destination):
        log.info('makedirs %s' % destination)
        os.makedirs(destination)
    elif not os.path.isdir(destination):
        init.parser.error("destination isn't a directory")
    
    log.info('mkdir %s/.templates/' % destination)
    os.makedirs(p.join(destination, '.templates'))
    log.info('mkdir %s/static/' % destination)
    os.makedirs(p.join(destination, 'static'))
    log.info('mkdir %s/wiki/' % destination)
    os.makedirs(p.join(destination, 'wiki'))
    
    log.info('Creating markdoc.yaml file')
    config_filename = p.join(destination, 'markdoc.yaml')
    fp = open(config_filename, 'w')
    try:
        fp.write('{}\n')
    finally:
        fp.close()
    
    log.info('Wiki initialization complete')
    log.info('Your new wiki is at: %s' % destination)

init.parser.add_argument('destination')


## Cleanup

@command
def clean_html(config, args):
    """Clean built HTML from the HTML root."""
    
    log = logging.getLogger('markdoc.clean-html')
    
    if p.exists(config.html_dir):
        log.info('rm -Rf %s' % config.html_dir)
        shutil.rmtree(config.html_dir)
    
    log.info('makedirs %s' % config.html_dir)
    os.makedirs(config.html_dir)


@command
def clean_temp(config, args):
    """Clean built HTML from the temporary directory."""
    
    log = logging.getLogger('markdoc.clean-temp')
    
    if p.exists(config.temp_dir):
        log.info('rm -Rf %s' % config.temp_dir)
        shutil.rmtree(config.temp_dir)
    
    log.info('makedirs %s' % config.temp_dir)
    os.makedirs(config.temp_dir)


## Synchronization

@command
def sync_static(config, args):
    """Sync static files into the HTML root."""
    
    log = logging.getLogger('markdoc.sync-static')
    
    if not p.exists(config.html_dir):
        log.info('makedirs %s' % config.html_dir)
        os.makedirs(config.html_dir)
    
    command = 'rsync -vaxq --ignore-errors --exclude=".*" --exclude="_*"'.split()
    display_cmd = command[:]
    
    if config.setdefault('use-default-static', True):
        # rsync needs the paths to have trailing slashes to work correctly.
        command.append(p.join(markdoc.default_static_dir, ''))
        display_cmd.append(p.basename(markdoc.default_static_dir) + '/')
    
    if p.isdir(config.static_dir):
        command.append(p.join(config.static_dir, ''))
        display_cmd.append(p.basename(config.static_dir) + '/')
    
    command.append(p.join(config.html_dir, ''))
    display_cmd.append(p.basename(config.html_dir) + '/')
    
    log.info(subprocess.list2cmdline(display_cmd))
    
    subprocess.check_call(command)
    
    log.info('rsync completed')


@command
def sync_html(config, args):
    """Sync built HTML and static media into the HTML root."""
    
    log = logging.getLogger('markdoc.sync-html')
    
    if not p.exists(config.html_dir):
        log.info('makedirs %s' % config.html_dir)
        os.makedirs(config.html_dir)
    
    command = 'rsync -vaxq --delete --ignore-errors --exclude=".*" --exclude="_*"'.split()
    display_cmd = command[:]
    
    # rsync needs the paths to have trailing slashes to work correctly.
    command.append(p.join(config.temp_dir, ''))
    display_cmd.append(p.basename(config.temp_dir) + '/')
    
    if config.setdefault('use-default-static', True):
        command.append(p.join(markdoc.default_static_dir, ''))
        display_cmd.append(p.basename(markdoc.default_static_dir) + '/')
    
    if p.isdir(config.static_dir):
        command.append(p.join(config.static_dir, ''))
        display_cmd.append(p.basename(config.static_dir) + '/')
    
    command.append(p.join(config.html_dir, ''))
    display_cmd.append(p.basename(config.html_dir) + '/')
    
    log.info(subprocess.list2cmdline(display_cmd))
    
    subprocess.check_call(command)
    
    log.info('rsync completed')


## Building

@command
def build(config, args):
    """Compile wiki to HTML and sync to the HTML root."""
    
    log = logging.getLogger('markdoc.build')
    
    clean_temp(config, args)
    
    builder = Builder(config)
    for rel_filename in builder.walk():
        html = builder.render_document(rel_filename)
        out_filename = p.join(config.temp_dir,
            p.splitext(rel_filename)[0] + p.extsep + 'html')
        
        if not p.exists(p.dirname(out_filename)):
            log.info('makedirs %s' % p.dirname(out_filename))
            os.makedirs(p.dirname(out_filename))
        
        log.info('Creating %s' % p.relpath(out_filename, start=config.temp_dir))
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
    
    log = logging.getLogger('markdoc.build-listing')
    
    list_basename = config.setdefault('listing-filename', '_list.html')
    builder = Builder(config)
    generate_listing = config.get('generate-listing', 'always').lower()
    always_list = True
    if generate_listing == 'never':
        log.info("No listing generated (generate-listing == never)")
        return # No need to continue.
    
    for fs_dir, _, _ in os.walk(config.html_dir):
        index_file_exists = any([
            p.exists(p.join(fs_dir, 'index.html')),
            p.exists(p.join(fs_dir, 'index'))])
        
        directory = '/' + '/'.join(p.relpath(fs_dir, start=config.html_dir).split(p.sep))
        if directory == '/' + p.curdir:
            directory = '/'
        
        if (generate_listing == 'sometimes') and index_file_exists:
            log.info("No listing generated for %s" % directory)
            continue
        
        log.info("Generating listing for %s" % directory)
        listing = builder.render_listing(directory)
        list_filename = p.join(fs_dir, list_basename)
        
        fp = codecs.open(list_filename, 'w', encoding='utf-8')
        try:
            fp.write(listing)
        finally:
            fp.close()
        
        if not index_file_exists:
            log.info("cp %s/%s %s/%s" % (directory, list_basename, directory, 'index.html'))
            shutil.copyfile(list_filename, p.join(fs_dir, 'index.html'))

## Serving

IPV4_RE = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')

@command
def serve(config, args):
    """Serve the built HTML from the HTML root."""
    
    # This should be a lazy import, otherwise it'll slow down the whole CLI.
    from markdoc.wsgi import MarkdocWSGIApplication
    
    log = logging.getLogger('markdoc.serve')
    app = MarkdocWSGIApplication(config)
    
    extra_config = {}
    if args.port:
        extra_config['port'] = args.port
    if args.interface:
        if not IPV4_RE.match(args.interface):
            serve.parser.error('invalid interface specifier: %r' % args.interface)
        extra_config['bind'] = args.interface
    
    server = config.server_maker(**extra_config)(app)
    
    try:
        log.info('Serving on http://%s:%d' % server.bind_addr)
        server.start()
    except KeyboardInterrupt:
        log.info('Interrupted')
    finally:
        log.info('Shutting down gracefully')
        server.stop()

serve.parser.add_argument('-p', '--port', type=int, default=None,
    help="Listen on specified port (default is 8008)")
serve.parser.add_argument('-i', '--interface', default=None,
    help="Bind to specified interface (defaults to loopback only)")
