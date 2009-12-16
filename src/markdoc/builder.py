# -*- coding: utf-8 -*-

import os
import os.path as p
import operator
import re

from markdoc.cache import DocumentCache, RenderCache, read_from
from markdoc.config import Config
from markdoc.render import make_relative


Config.register_default('listing-filename', '_list.html')


class Builder(object):
    
    """An object to handle all the parts of the wiki building process."""
    
    def __init__(self, config):
        self.config = config
        
        self.doc_cache = DocumentCache(base=self.config.wiki_dir)
        
        def render_func(path, doc):
            level = len(path.lstrip('/').split('/')) - 1
            return self.config.markdown(curr_path=path).convert(doc)
        self.render_cache = RenderCache(render_func, self.doc_cache)
        
        render_doc_func = lambda path, doc: self.render_document(path, cache=False)
        self.document_render_cache = RenderCache(render_doc_func, self.render_cache)
    
    def crumbs(self, path):
        
        """
        Produce a breadcrumbs list for the given filename.
        
        The crumbs are calculated based on the wiki root and the absolute path
        to the current file.
        
        Examples
        --------
        
        Assuming a wiki root of `/a/b/c`:
        
        * `a/b/c/wiki/index.md` => `[('index', None)]`
        
        * `a/b/c/wiki/subdir/index.md` =>
          `[('index', '/'), ('subdir', None)]`
        
        * `a/b/c/wiki/subdir/file.md` =>
          `[('index', '/'), ('subdir', '/subdir/'), ('file', None)]
        
        """
        
        if p.isabs(path):
            path = self.doc_cache.relative(path)
        
        rel_components = path.split(p.sep)
        terminus = p.splitext(rel_components.pop())[0]
        
        if not rel_components:
            if terminus == 'index':
                return [('index', None)]
            return [('index', '/'), (terminus, None)]
        elif terminus == 'index':
            terminus = p.splitext(rel_components.pop())[0]
        
        crumbs = [('index', '/')]
        for component in rel_components:
            path = '%s%s/' % (crumbs[-1][1], component)
            crumbs.append((component, path))
        
        crumbs.append((terminus, None))
        return crumbs
    
    def walk(self):
        
        """
        Walk through the wiki, yielding info for each document.
        
        For each document encountered, a `(filename, crumbs)` tuple will be
        yielded.
        """
        
        if not self.config['document-extensions']:
            self.config['document-extensions'].append('')
        
        def valid_extension(filename):
            return any(filename.endswith(valid_ext)
                       for valid_ext in self.config['document-extensions'])
        
        for dirpath, subdirs, files in os.walk(self.config.wiki_dir):
            remove_hidden(subdirs); subdirs.sort()
            remove_hidden(files); files.sort()
            
            for filename in filter(valid_extension, files):
                full_filename = p.join(dirpath, filename)
                yield p.relpath(full_filename, start=self.config.wiki_dir)
    
    def listing_context(self, directory):
        
        """
        Generate the template context for a directory listing.
        
        This method accepts a relative path, with the base assumed to be the
        HTML root. This means listings must be generated after the wiki is
        built, allowing them to list static media too. 
        
        Directories should always be '/'-delimited when specified, since it is
        assumed that they are URL paths, not filesystem paths.
        
        For information on what the produced context will look like, consult the
        `listing` doctest.
        """
        
        # Ensure the directory name ends with '/'. 
        directory = directory.strip('/')
        
        # Resolve to filesystem paths.
        fs_rel_dir = p.sep.join(directory.split('/'))
        fs_abs_dir = p.join(self.config.html_dir, fs_rel_dir)
        skip_files = set([self.config['listing-filename'], 'index.html'])
        
        sub_directories, pages, files = [], [], []
        for basename in os.listdir(fs_abs_dir):
            fs_abs_path = p.join(fs_abs_dir, basename)
            file_dict = {
                'basename': basename,
                'href': directory + '/' + basename}
            if not file_dict['href'].startswith('/'):
                file_dict['href'] = '/' + file_dict['href']
            
            if p.isdir(fs_abs_path):
                file_dict['href'] += '/'
                sub_directories.append(file_dict)
            
            else:
                if (basename in skip_files or basename.startswith('.') or
                    basename.startswith('_')):
                    continue
                
                file_dict['slug'] = p.splitext(basename)[0]
                file_dict['size'] = p.getsize(fs_abs_path)
                file_dict['humansize'] = humansize(file_dict['size'])
                
                if p.splitext(basename)[1] == (p.extsep + 'html'):
                    # Get the title from the file.
                    contents = read_from(fs_abs_path)
                    file_dict['title'] = get_title(file_dict['slug'], contents)
                    # Remove .html from the end of the href.
                    file_dict['href'] = p.splitext(file_dict['href'])[0]
                    pages.append(file_dict)
                else:
                    files.append(file_dict)
        
        sub_directories.sort(key=lambda directory: directory['basename'])
        pages.sort(key=lambda page: page['title'])
        files.sort(key=lambda file_: file_['basename'])
        
        return {
            'directory': directory,
            'sub_directories': sub_directories,
            'pages': pages,
            'files': files,
            'make_relative': lambda href: make_relative(directory, href),
        }
    
    def render(self, path, cache=True):
        return self.render_cache.render(path, cache=cache)
    
    def title(self, path, cache=True):
        return get_title(path, self.render(path, cache=cache))
    
    def render_document(self, path, cache=True):
        if cache:
            return self.document_render_cache.render(path)
        
        context = {}
        context['content'] = self.render(path)
        context['title'] = self.title(path)
        context['crumbs'] = self.crumbs(path)
        context['make_relative'] = lambda href: make_relative(path, href)
        
        template = self.config.template_env.get_template('document.html')
        return template.render(context)
    
    def render_listing(self, path):
        import jinja2
        
        context = self.listing_context(path)
        
        crumbs = [('index', '/')]
        if path not in ['', '/']:
            current_dir = ''
            for component in path.strip('/').split('/'):
                crumbs.append((component, '%s/%s/' % (current_dir, component)))
                current_dir += '/' + component
        crumbs.append((jinja2.Markup('<span class="list-crumb">list</span>'), None))
        
        context['crumbs'] = crumbs
        context['make_relative'] = lambda href: make_relative(path + '/', href)
        
        template = self.config.template_env.get_template('listing.html')
        return template.render(context)


def remove_hidden(names):
    """Remove (in-place) all strings starting with a '.' in the given list."""
    
    i = 0
    while i < len(names):
        if names[i].startswith('.'):
            names.pop(i)
        else:
            i += 1
    return names


def get_title(filename, data):
    """Try to retrieve a title from a filename and its contents."""
    
    match = re.search(r'<!-- ?title:(.+)-->', data, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', data, re.IGNORECASE)
    if match:
        return match.group(1)
    
    name, extension = p.splitext(p.basename(filename))
    return re.sub(r'[-_]+', ' ', name).title()


def humansize(size, base=1024):
    import decimal
    import math
    
    if size == 0:
        return '0B'
    
    i = int(math.log(size, base))
    prefix = 'BKMGTPEZY'[i]
    number = decimal.Decimal(size) / (base ** i)
    return str(number.to_integral()) + prefix
