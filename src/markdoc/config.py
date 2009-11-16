# -*- coding: utf-8 -*-

"""Utilities for working with Markdoc configurations."""

import os

import cherrypy.wsgiserver
import jinja2
import markdown
import yaml

import markdoc.exc


class ConfigNotFound(markdoc.exc.AbortError):
    """The configuration file was not found."""
    pass


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
    
    def __init__(self, config_file, config):
        super(Config, self).__init__(config)
        
        self['document-extensions'] = set(self.get('document-extensions',
            ['.md', '.mdown', '.markdown', '.wiki', '.text']))
        
        meta = self.setdefault('meta', {})
        meta['config_file'] = config_file
        if 'root' not in meta:
            meta['root'] = os.path.dirname(config_file)
    
    @property
    def html_dir(self):
        self.setdefault('hide-prefix', '.')
        return os.path.join(self['meta']['root'], self['hide-prefix'] + 'html')
    
    @property
    def static_dir(self):
        return os.path.join(self['meta']['root'], 'static')
    
    @property
    def wiki_dir(self):
        return os.path.join(self['meta']['root'], 'wiki')
    
    @property
    def temp_dir(self):
        self.setdefault('hide-prefix', '.')
        return os.path.join(self['meta']['root'], self['hide-prefix'] + 'tmp')
    
    @property
    def template_dir(self):
        self.setdefault('hide-prefix', '.')
        return os.path.join(self['meta']['root'], self['hide-prefix'] + 'templates')
    
    @classmethod
    def for_directory(cls, directory=None):
        
        """
        Get the configuration from the 'markdoc.yaml' file in a directory.
        
        If you do not specify a directory, this method will use the current
        working directory.
        """
        
        if directory is None:
            directory = os.getcwd()
        
        filename = os.path.join(directory, 'markdoc.yaml')
        return cls.for_file(filename)
    
    @classmethod
    def for_file(cls, filename):
        """Get the configuration from a given YAML file."""
        
        if not os.path.exists(filename):
            relpath = os.path.relpath(os.path.dirname(filename), start=os.getcwd())
            basename = os.path.basename(filename)
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
            loader = jinja2.FileSystemLoader(self.template_dir)
            environment = jinja2.Environment(loader=loader)
            environment.globals['config'] = self
            self.__template_env = environment
        return self.__template_env
    
    def markdown(self, **config):
        """Return a `markdown.Markdown` instance for this configuration."""
        
        # Set up the default markdown configuration.
        mdconfig = self.setdefault('markdown', {})
        mdconfig.setdefault('extensions', [])
        mdconfig.setdefault('extension_configs', {})
        mdconfig.setdefault('safe_mode', False)
        mdconfig.setdefault('output_format', 'xhtml1')
        
        config.update(mdconfig) # Include any extra kwargs.
        return markdown.Markdown(**mdconfig)
    
    def server_maker(self, **config):
        
        """
        Return a server-making callable to create a CherryPy WSGI server.
        
        The server-making callable should be passed a WSGI application, and it
        will return an instance of `cherrypy.wsgiserver.CherryPyWSGIServer`.
        """
        
        svconfig = self.setdefault('server', {})
        bind = svconfig.setdefault('bind', '127.0.0.1')
        port = svconfig.setdefault('port', 8008)
        num_threads = svconfig.setdefault('num_threads', 10)
        server_name = svconfig.setdefault('server_name', None)
        request_queue_size = svconfig.setdefault('request_queue_size', 5)
        timeout = svconfig.setdefault('timeout', 10)
        
        bind_addr = (bind, port)
        kwargs = {
            'num_threads': threads,
            'server_name': server_name,
            'request_queue_size': request_queue_size,
            'timeout': timeout}
        
        return lambda wsgi_app: cherrypy.wsgiserver.CherryPyWSGIServer(bind_addr, wsgi_app, **kwargs)
