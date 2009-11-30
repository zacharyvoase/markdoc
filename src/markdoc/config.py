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
        return cls
    
    def register_default(cls, key, default_value):
        cls._defaults[key] = default_value


class Config(dict):
    
    """
    A dictionary which represents a single wiki's Markdoc configuration.
    
    When instantiating this dictionary, if you aren't using an actual
    configuration file, just remember to set `config['meta']['root']` to the
    wiki root; you can use `None` as the value for config_file. For example:
        
        # With a filename:
        config = Config('filename.yaml', {...})
        
        # Without a filename:
        config = Config(None, {'meta': {'root': '/path/to/wiki/root/'}, ...})
    
    """
    
    __metaclass__ = ConfigMeta
    
    def __init__(self, config_file, config):
        super(Config, self).__init__(config)
        
        self['document-extensions'] = set(self.get('document-extensions',
            ['.md', '.mdown', '.markdown', '.wiki', '.text']))
        
        if not self['document-extensions']:
            self['document-extensions'].add('')
        
        meta = self.setdefault('meta', {})
        meta['config_file'] = config_file
        if 'root' not in meta:
            meta['root'] = p.dirname(config_file)
    
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if key in self._defaults:
                self[key] = copy.copy(self._defaults[key])
                return self[key]
            raise
    
    def __delitem__(self, key):
        if (key not in self) and (key in self._defaults):
            return
        return dict.__delitem__(self, key)
    
    @property
    def html_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'],
            self.get('html-dir', self['hide-prefix'] + 'html'))
    
    @property
    def static_dir(self):
        return p.join(self['meta']['root'], self.get('static-dir', 'static'))
    
    @property
    def wiki_dir(self):
        return p.join(self['meta']['root'], self.get('wiki-dir', 'wiki'))
    
    @property
    def temp_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'],
            self.get('temp-dir', self['hide-prefix'] + 'tmp'))
    
    @property
    def template_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'],
            self.get('template-dir', self['hide-prefix'] + 'templates'))
    
    @classmethod
    def for_directory(cls, directory=None):
        
        """
        Get the configuration from the 'markdoc.yaml' file in a directory.
        
        If you do not specify a directory, this method will use the current
        working directory.
        """
        
        if directory is None:
            directory = os.getcwd()
        
        filename = p.join(directory, 'markdoc.yaml')
        return cls.for_file(filename)
    
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
    
    @property
    def template_env(self):
        if not getattr(self, '__template_env', None):
            # Lazy import to save time when running the `markdoc` command.
            import jinja2
            
            loader_path = []
            if p.isdir(self.template_dir):
                loader_path.append(self.template_dir)
            if self.setdefault('use-default-templates', True):
                loader_path.append(markdoc.default_template_dir)
            loader = jinja2.FileSystemLoader(loader_path)
            
            environment = jinja2.Environment(loader=loader)
            environment.globals['config'] = self
            
            self.__template_env = environment
        
        return self.__template_env
    
    def markdown(self, **config):
        """Return a `markdown.Markdown` instance for this configuration."""
        
        # Set up the default markdown configuration.
        mdconfig = self.setdefault('markdown', {})
        mdconfig.setdefault('extensions', [])
        mdconfig.setdefault('extension_configs', mdconfig.get('extension-configs', {}))
        mdconfig.setdefault('safe_mode', mdconfig.get('safe-mode', False))
        mdconfig.setdefault('output_format', mdconfig.get('output-format', 'xhtml1'))
        
        config.update(mdconfig) # Include any extra kwargs.
        return markdown.Markdown(**mdconfig)
    
    def server_maker(self, **extra_config):
        
        """
        Return a server-making callable to create a CherryPy WSGI server.
        
        The server-making callable should be passed a WSGI application, and it
        will return an instance of `cherrypy.wsgiserver.CherryPyWSGIServer`.
        
        You can optionally override any of the hardwired configuration
        parameters by passing in keyword arguments which will be passed along to
        the `CherryPyWSGIServer` constructor.
        """
        
        # Lazy import, to save time for non-server commands.
        import cherrypy.wsgiserver
        
        svconfig = self.setdefault('server', {})
        
        def get_conf(key, default):
            return svconfig.setdefault(key,
                # Look for `some-key` as well as `some_key`.
                svconfig.get(key.replace('_', '-'),
                    extra_config.pop(key, default)))
        
        bind = get_conf('bind', '127.0.0.1')
        port = get_conf('port', 8008)
        numthreads = get_conf('numthreads', get_conf('num_threads', 10))
        server_name = get_conf('server_name', None)
        request_queue_size = get_conf('request_queue_size', 5)
        timeout = get_conf('timeout', 10)
        
        bind_addr = (bind, port)
        kwargs = {
            'numthreads': numthreads,
            'server_name': server_name,
            'request_queue_size': request_queue_size,
            'timeout': timeout}
        kwargs.update(extra_config)
        
        return lambda wsgi_app: cherrypy.wsgiserver.CherryPyWSGIServer(bind_addr, wsgi_app, **kwargs)
