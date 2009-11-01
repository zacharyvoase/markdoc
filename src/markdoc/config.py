# -*- coding: utf-8 -*-

"""Utilities for working with Markdoc configurations."""

import os

import cherrypy.wsgiserver
import markdown
import yaml

import markdoc.exc


class ConfigNotFound(markdoc.exc.AbortError):
    """The configuration file was not found."""
    pass


class MarkdocConfig(dict):
    
    """A dictionary which represents the Markdoc configuration."""
    
    def __init__(self, config_file, config):
        super(MarkdocConfig, self).__init__(config)
        self.setdefault('meta', {})['config_file'] = config_file
    
    @classmethod
    def for_directory(cls, directory=None):
        
        """
        Get the configuration from the 'markdoc.yaml' file in a directory.
        
        If you do not specify a directory, this method will use the current
        working directory.
        """
        
        if directory is None:
            directory = os.getcwd()
        
        config_file = os.path.join(directory, 'markdoc.yaml')
        
        if not os.path.exists(config_file):
            relpath = os.path.relpath(directory)
            if relpath == '.':
                raise ConfigNotFound("markdoc.yaml was not found in the current directory")
            raise ConfigNotFound("markdoc.yaml was not found in %s" % relpath)
        
        fp = open(config_file)
        try:
            config = yaml.load(fp)
        finally:
            fp.close()
        
        return cls(config_file, config)
    
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
