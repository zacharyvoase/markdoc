# -*- coding: utf-8 -*-

import codecs
from functools import wraps
import os
import os.path as p
import time


class DocumentCache(object):
    
    """
    A high-level document cache for caching the content of files.
    
    This is a read-only cache which uses the OS-reported modification timestamps
    for files (via `os.stat()`) to determine cache dirtiness, and then refreshes
    its cache behind the scenes when files are requested.
    
    You can access values via `.get()` (which supports several options) or via
    simple subscription syntax (i.e. `cache[path]`). The cache is configured
    with a 'root' on instantiation, by which all relative paths are resolved.
    """
    
    def __init__(self, base=None, cache=None, encoding='utf-8'):
        if cache is None:
            cache = {}
        self.cache = cache
        
        if base is None:
            base = os.getcwd()
        self.base = base
        
        self.encoding = encoding
    
    absolute = lambda self, relpath: p.join(self.base, relpath)
    relative = lambda self, abspath: p.relpath(abspath, start=self.base)
    
    def has_latest_version(self, path):
        """Determine whether the cache for a path is up to date."""
        
        # No-op for already-absolute paths.
        path = self.absolute(path)
        if path not in self.cache:
            return False
        cached_mtime = self.cache[path][0]
        return os.stat(path).st_mtime <= cached_mtime
    
    def refresh_cache(self, path, encoding=None):
        """Refresh the cache, no matter what, with an optional encoding."""
        
        path = self.absolute(path)
        encoding = encoding or self.encoding
        data = read_from(path, encoding=encoding)
        mtime = os.stat(path).st_mtime
        self.cache[path] = (mtime, data)
    
    def update_to_latest_version(self, path):
        """If necessary, refresh the cache's copy of a file."""
        
        if not self.has_latest_version(path):
            self.refresh_cache(path)
    
    def get(self, path, cache=True, encoding=None):
        """Retrieve the data for a given path, optionally using the cache."""
        
        path = self.absolute(path)
        
        if cache:
            self.update_to_latest_version(path)
            return self.cache[path][1] # (mtime, data)[1]
        
        if not p.isfile(path):
            return None
        
        if encoding is None:
            encoding = self.encoding
        return read_from(path, encoding=encoding)
    
    def __getitem__(self, path):
        result = self.get(path)
        if result is None:
            raise KeyError(path)
        return result


def read_from(filename, encoding='utf-8'):
    """Read data from a filename, optionally with an encoding."""
    
    if encoding is None:
        fp = open(filename)
    else:
        fp = codecs.open(filename, encoding=encoding)
    
    try:
        return fp.read()
    finally:
        fp.close()
