# -*- coding: utf-8 -*-

"""Utilities for working with Markdoc configurations."""

import copy
import os
import os.path as p

import markdown
import yaml

import markdoc.exc


class ConfigNotFound(markdoc.exc.AbortError):
    """The configuration file was not found."""
    pass


class ConfigMeta(type):
    
    def __new__(mcls, name, bases, attrs):
        cls = type.__new__(mcls, name, bases, attrs)
        cls._defaults = {}
        cls._func_defaults = {}
        return cls
    
    def register_default(cls, key, default_value):
        """Register a default value for a given key."""
        
        cls._defaults[key] = default_value
    
    def register_func_default(cls, key, function):
        """Register a callable as a functional default for a key."""
        
        cls._func_defaults[key] = function
    
    def func_default_for(cls, key):
        """Decorator to define a functional default for a given key."""
        
        return lambda function: [cls.register_func_default(key, function),
                                 function][1]


class Config(dict):
    
    """
    A dictionary which represents a single wiki's Markdoc configuration.
    
    When instantiating this dictionary, if you aren't using an actual
    configuration file, just remember to set `config['meta.root']` to the
    wiki root; you can use `None` as the value for config_file. For example:
        
        # With a filename:
        config = Config('filename.yaml', {...})
        
        # Without a filename:
        config = Config(None, {'meta': {'root': '/path/to/wiki/root/'}, ...})
    
    """
    
    __metaclass__ = ConfigMeta
    
    def __init__(self, config_file, config):
        super(Config, self).__init__(flatten(config))
        
        self['meta.config-file'] = config_file
        self['meta.root'] = p.dirname(config_file)
    
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if key in self._defaults:
                self[key] = copy.copy(self._defaults[key])
            elif key in self._func_defaults:
                self[key] = self._func_defaults[key](self, key)
            else:
                raise
            return dict.__getitem__(self, key)
    
    def __delitem__(self, key):
        if (key not in self):
            return # fail silently.
        return dict.__delitem__(self, key)
    
    @classmethod
    def for_directory(cls, directory=None):
        
        """
        Get the configuration from the 'markdoc.yaml' file in a directory.
        
        If you do not specify a directory, this method will use the current
        working directory.
        """
        
        if directory is None:
            directory = os.getcwd()
        
        if p.exists(p.join(directory, 'markdoc.yaml')):
            return cls.for_file(p.join(directory, 'markdoc.yaml'))
        elif p.exists(p.join(directory, '.markdoc.yaml')):
            return cls.for_file(p.join(directory, '.markdoc.yaml'))
        raise ConfigNotFound("A markdoc configuration could not be found.")
    
    @classmethod
    def for_file(cls, filename):
        """Get the configuration from a given YAML file."""
        
        if not p.exists(filename):
            relpath = p.relpath(p.dirname(filename), start=os.getcwd())
            basename = p.basename(filename)
            if relpath == '.':
                raise ConfigNotFound("%s was not found in the current directory" % basename)
            raise ConfigNotFound("%s was not found in %s" % (basename, relpath))
        
        fp = open(filename)
        try:
            config = yaml.load(fp) or {}
        finally:
            fp.close()
        
        return cls(filename, config)


def flatten(dictionary, prefix=''):
    
    """
    Flatten nested dictionaries into dotted keys.
    
        >>> d = {
        ...     'a': {
        ...           'b': 1,
        ...           'c': {
        ...                 'd': 2,
        ...                 'e': {
        ...                       'f': 3
        ...                 }
        ...           }
        ...      },
        ...      'g': 4,
        ... }
    
        >>> sorted(flatten(d).items())
        [('a.b', 1), ('a.c.d', 2), ('a.c.e.f', 3), ('g', 4)]
    """
    
    for key in dictionary.keys():
        value = dictionary.pop(key)
        if not isinstance(value, dict):
            dictionary[prefix + key] = value
        else:
            for key2 in value.keys():
                value2 = value.pop(key2)
                if not isinstance(value2, dict):
                    dictionary[prefix + key + '.' + key2] = value2
                else:
                    dictionary.update(flatten(value2,
                        prefix=(prefix + key + '.' + key2 + '.')))
    return dictionary
