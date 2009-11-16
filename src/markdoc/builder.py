# -*- coding: utf-8 -*-

import os
import operator
import re

from markdoc.cache import DocumentCache, RenderCache


class Builder(object):
    
    """An object to handle all the parts of the wiki building process."""
    
    def __init__(self, config):
        self.config = config
        self.doc_cache = DocumentCache(base=os.path.join(self.config['meta']['root'], 'wiki'))
        render_func = lambda doc: self.config.markdown().convert(doc)
        self.render_cache = RenderCache(render_func, self.doc_cache)
    
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
        
        if os.path.isabs(path):
            path = self.doc_cache.relative(path)
        
        rel_components = path.split(os.path.sep)
        terminus = os.path.splitext(rel_components.pop())[0]
        
        if not rel_components:
            return [(terminus, None)]
        elif terminus == 'index':
            terminus = os.path.splitext(rel_components.pop())[0]
        
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
        
        wiki_dir = os.path.join(self.config['meta']['root'], 'wiki')
        
        for dirpath, subdirs, files in os.walk(wiki_dir):
            remove_hidden(subdirs); subdirs.sort()
            remove_hidden(files); files.sort()
            
            for filename in files:
                name, extension = os.path.splitext(filename)
                if extension in self.config['document-extensions']:
                    full_filename = os.path.join(dirpath, filename)
                    yield os.path.relpath(full_filename, start=self.doc_cache.base)
    
    def render(self, path, cache=True):
        return self.render_cache.render(path, cache=cache)
    
    def title(self, path, cache=True):
        return get_title(path, self.render(path, cache=cache))
    
    def render_document(self, path):
        context = {}
        context['content'] = self.render(path)
        context['title'] = self.title(path)
        context['crumbs'] = self.crumbs(path)
        
        template = self.config.template_env.get_template('document.html')
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
    
    name, extension = os.path.splitext(os.path.basename(filename))
    return re.sub(r'[-_]+', ' ', name).title()
