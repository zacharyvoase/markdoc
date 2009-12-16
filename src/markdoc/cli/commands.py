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
import sys

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
        logging.getLogger('markdoc').debug('Running markdoc.%s' % cmd_name)
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
    
    if p.exists(destination) and os.listdir(destination):
        init.parser.error("destination isn't empty")
    elif not p.exists(destination):
        log.debug('makedirs %s' % destination)
        os.makedirs(destination)
    elif not p.isdir(destination):
        init.parser.error("destination isn't a directory")
    
    log.debug('mkdir %s/.templates/' % destination)
    os.makedirs(p.join(destination, '.templates'))
    log.debug('mkdir %s/static/' % destination)
    os.makedirs(p.join(destination, 'static'))
    log.debug('mkdir %s/wiki/' % destination)
    os.makedirs(p.join(destination, 'wiki'))
    
    log.debug('Creating markdoc.yaml file')
    config_filename = p.join(destination, 'markdoc.yaml')
    fp = open(config_filename, 'w')
    try:
        fp.write('{}\n')
    finally:
        fp.close()
    
    if args.vcs_ignore:
        config = markdoc.config.Config.for_directory(destination)
        args = vcs_ignore.parser.parse_args([args.vcs_ignore])
        vcs_ignore(config, args)
    
    log.info('Wiki initialization complete')
    log.info('Your new wiki is at: %s' % destination)

init.parser.add_argument('destination', default=None,
    help="Create wiki here (if omitted, defaults to current directory)")
init.parser.add_argument('--vcs-ignore', choices=['hg', 'git', 'cvs', 'bzr'],
    help="Create an ignore file for the specified VCS.")


@command
def vcs_ignore(config, args):
    """Create a VCS ignore file for a wiki."""
    
    log = logging.getLogger('markdoc.vcs-ignore')
    log.debug('Creating ignore file for %s' % args.vcs)
    wiki_root = config['meta.root'] # shorter local alias.
    
    ignore_file_lines = []
    ignore_file_lines.append(p.relpath(config.html_dir, start=wiki_root))
    ignore_file_lines.append(p.relpath(config.temp_dir, start=wiki_root))
    if args.vcs == 'hg':
        ignore_file_lines.insert(0, 'syntax: glob')
        ignore_file_lines.insert(1, '')
    
    if args.output == '-':
        log.debug('Writing ignore file to stdout')
        fp = sys.stdout
    else:
        if not args.output:
            filename = p.join(wiki_root, '.%signore' % args.vcs)
        else:
            filename = p.join(wiki_root, args.output)
        log.info('Writing ignore file to %s' % p.relpath(filename, start=wiki_root))
        fp = open(filename, 'w')
    
    try:
        fp.write('\n'.join(ignore_file_lines) + '\n')
    finally:
        if fp is not sys.stdout:
            fp.close()
    
    log.debug('Ignore file written.')

vcs_ignore.parser.add_argument('vcs', default='hg', nargs='?',
    choices=['hg', 'git', 'cvs', 'bzr'],
    help="Create ignore file for specified VCS (default 'hg')")
vcs_ignore.parser.add_argument('-o', '--output', default=None, metavar='FILENAME',
    help="Write output to the specified filename, relative to the wiki root. "
         "Default is to generate the filename from the VCS. "
         "'-' will write to stdout.")


## Cleanup

@command
def clean_html(config, args):
    """Clean built HTML from the HTML root."""
    
    log = logging.getLogger('markdoc.clean-html')
    
    if p.exists(config.html_dir):
        log.debug('rm -Rf %s' % config.html_dir)
        shutil.rmtree(config.html_dir)
    
    log.debug('makedirs %s' % config.html_dir)
    os.makedirs(config.html_dir)


@command
def clean_temp(config, args):
    """Clean built HTML from the temporary directory."""
    
    log = logging.getLogger('markdoc.clean-temp')
    
    if p.exists(config.temp_dir):
        log.debug('rm -Rf %s' % config.temp_dir)
        shutil.rmtree(config.temp_dir)
    
    log.debug('makedirs %s' % config.temp_dir)
    os.makedirs(config.temp_dir)


## Synchronization

@command
def sync_static(config, args):
    """Sync static files into the HTML root."""
    
    log = logging.getLogger('markdoc.sync-static')
    
    if not p.exists(config.html_dir):
        log.debug('makedirs %s' % config.html_dir)
        os.makedirs(config.html_dir)
    
    command = ('rsync -vaxq --ignore-errors --exclude=.* --exclude=_*').split()
    display_cmd = command[:]
    
    if config['use-default-static']:
        # rsync needs the paths to have trailing slashes to work correctly.
        command.append(p.join(markdoc.default_static_dir, ''))
        display_cmd.append(p.basename(markdoc.default_static_dir) + '/')
    
    if p.isdir(config.static_dir):
        command.append(p.join(config.static_dir, ''))
        display_cmd.append(p.basename(config.static_dir) + '/')
    
    command.append(p.join(config.html_dir, ''))
    display_cmd.append(p.basename(config.html_dir) + '/')
    
    log.debug(subprocess.list2cmdline(display_cmd))
    
    subprocess.check_call(command)
    
    log.debug('rsync completed')


@command
def sync_html(config, args):
    """Sync built HTML and static media into the HTML root."""
    
    log = logging.getLogger('markdoc.sync-html')
    
    if not p.exists(config.html_dir):
        log.debug('makedirs %s' % config.html_dir)
        os.makedirs(config.html_dir)
    
    command = ('rsync -vaxq --delete --ignore-errors --exclude=.* --exclude=_*').split()
    display_cmd = command[:]
    
    # rsync needs the paths to have trailing slashes to work correctly.
    command.append(p.join(config.temp_dir, ''))
    display_cmd.append(p.basename(config.temp_dir) + '/')
    
    if config['use-default-static']:
        command.append(p.join(markdoc.default_static_dir, ''))
        display_cmd.append(p.basename(markdoc.default_static_dir) + '/')
    
    if p.isdir(config.static_dir):
        command.append(p.join(config.static_dir, ''))
        display_cmd.append(p.basename(config.static_dir) + '/')
    
    command.append(p.join(config.html_dir, ''))
    display_cmd.append(p.basename(config.html_dir) + '/')
    
    log.debug(subprocess.list2cmdline(display_cmd))
    
    subprocess.check_call(command)
    
    log.debug('rsync completed')


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
            log.debug('makedirs %s' % p.dirname(out_filename))
            os.makedirs(p.dirname(out_filename))
        
        log.debug('Creating %s' % p.relpath(out_filename, start=config.temp_dir))
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
    
    list_basename = config['listing-filename']
    builder = Builder(config)
    generate_listing = config.get('generate-listing', 'always').lower()
    always_list = True
    if generate_listing == 'never':
        log.debug("No listing generated (generate-listing == never)")
        return # No need to continue.
    
    for fs_dir, _, _ in os.walk(config.html_dir):
        index_file_exists = any([
            p.exists(p.join(fs_dir, 'index.html')),
            p.exists(p.join(fs_dir, 'index'))])
        
        directory = '/' + '/'.join(p.relpath(fs_dir, start=config.html_dir).split(p.sep))
        if directory == '/' + p.curdir:
            directory = '/'
        
        if (generate_listing == 'sometimes') and index_file_exists:
            log.debug("No listing generated for %s" % directory)
            continue
        
        log.debug("Generating listing for %s" % directory)
        listing = builder.render_listing(directory)
        list_filename = p.join(fs_dir, list_basename)
        
        fp = codecs.open(list_filename, 'w', encoding='utf-8')
        try:
            fp.write(listing)
        finally:
            fp.close()
        
        if not index_file_exists:
            log.debug("cp %s/%s %s/%s" % (directory, list_basename, directory, 'index.html'))
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
    
    config['server.port'] = args.port
    config['server.num-threads'] = args.num_threads
    if args.server_name:
        config['server.name'] = args.server_name
    config['server.request-queue-size'] = args.queue_size
    config['server.timeout'] = args.timeout
    if args.interface:
        if not IPV4_RE.match(args.interface):
            serve.parser.error('invalid interface specifier: %r' % args.interface)
        config['server.bind'] = args.interface
    
    server = config.server_maker()(app)
    
    try:
        log.info('Serving on http://%s:%d' % server.bind_addr)
        server.start()
    except KeyboardInterrupt:
        log.debug('Interrupted')
    finally:
        log.info('Shutting down gracefully')
        server.stop()

serve.parser.add_argument('-p', '--port', type=int, default=8008,
    help="Listen on specified port (default is 8008)")
serve.parser.add_argument('-i', '--interface', default=None,
    help="Bind to specified interface (defaults to loopback only)")
serve.parser.add_argument('-t', '--num-threads', type=int, default=10, metavar='N',
    help="Use N threads to handle requests (default is 10)")
serve.parser.add_argument('-n', '--server-name', default=None, metavar='NAME',
    help="Use an explicit server name (default to an autodetected value)")
serve.parser.add_argument('-q', '--queue-size', type=int, default=5, metavar='SIZE',
    help="Set request queue size (default is 5)")
serve.parser.add_argument('--timeout', type=int, default=10,
    help="Set the socket timeout for connections (default is 10)")

