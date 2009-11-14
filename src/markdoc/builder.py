# -*- coding: utf-8 -*-

import os
import operator


class Builder(object):
    
    """An object to handle all the parts of the wiki building process."""
    
    def __init__(self, config):
        self.config = config
    
    def crumbs(self, filename):
        
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
        
        doc_root = os.path.join(self.config['meta']['root'], 'wiki')
        rel_path = os.path.relpath(filename, start=doc_root)
        rel_components = rel_path.split(os.path.sep)
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
                    yield (full_filename, self.crumbs(full_filename))


def remove_hidden(names):
    """Remove (in-place) all strings starting with a '.' in the given list."""
    
    i = 0
    while i < len(names):
        if names[i].startswith('.'):
            names.pop(i)
        else:
            i += 1
    return names
