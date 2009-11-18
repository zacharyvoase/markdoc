# -*- coding: utf-8 -*-

"""Utilities for working with Markdoc configurations."""

import os
import os.path as p

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
            meta['root'] = p.dirname(config_file)
    
    @property
    def html_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'], self['hide-prefix'] + 'html')
    
    @property
    def static_dir(self):
        return p.join(self['meta']['root'], 'static')
    
    @property
    def wiki_dir(self):
        return p.join(self['meta']['root'], 'wiki')
    
    @property
    def temp_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'], self['hide-prefix'] + 'tmp')
    
    @property
    def template_dir(self):
        self.setdefault('hide-prefix', '.')
        return p.join(self['meta']['root'], self['hide-prefix'] + 'templates')
    
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
        mdconfig.setdefault('extension_configs', {})
        mdconfig.setdefault('safe_mode', False)
        mdconfig.setdefault('output_format', 'xhtml1')
        
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
        get_conf = lambda key, default: svconfig.setdefault(key, extra_config.pop(key, default))
        
        bind = get_conf('bind', '127.0.0.1')
        port = get_conf('port', 8008)
        numthreads = get_conf('numthreads', 10)
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
