# -*- coding: utf-8 -*-

import codecs
import os
import os.path as p
import pprint
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
    elif generate_listing == 'sometimes':
        always_list = False
    
    for fs_dir, _, _ in os.walk(config.html_dir):
        rel_fs_dir = p.relpath(fs_dir, start=config.html_dir)
        directory = '/' + '/'.join(rel_fs_dir.replace(p.curdir, '').split(p.sep))
        
        index_file = None
        if p.exists(p.join(fs_dir, 'index.html')):
            index_file = p.join(fs_dir, 'index.html')
        elif p.exists(p.join(fs_dir, 'index')):
            index_file = p.join(fs_dir, 'index')
        
        if (not always_list) and (index_file is not None):
            continue
        
        context = builder.listing_context(directory)
        listing = config.template_env.get_template('listing.html').render(context)
        
        fp = codecs.open(p.join(fs_dir, list_basename), 'w', encoding='utf-8')
        try:
            fp.write(listing)
        finally:
            fp.close()
        
        if index_file is None:
            shutil.copyfile(p.join(fs_dir, list_basename), p.join(fs_dir, 'index.html'))
