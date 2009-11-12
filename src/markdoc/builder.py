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