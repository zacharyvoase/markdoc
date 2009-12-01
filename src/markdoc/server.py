# -*- coding: utf-8 -*-

from markdoc.config import Config


Config.register_default('server.bind', '127.0.0.1')
Config.register_default('server.port', 8008)
Config.register_default('server.num-threads', 10)
Config.register_default('server.name', None)
Config.register_default('server.request-queue-size', 5)
Config.register_default('server.timeout', 10)


def server_maker(config, **extra_config):
    
    """
    Return a server-making callable to create a CherryPy WSGI server.
    
    The server-making callable should be passed a WSGI application, and it
    will return an instance of `cherrypy.wsgiserver.CherryPyWSGIServer`.
    
    You can optionally override any of the hardwired configuration
    parameters by passing in keyword arguments which will be passed along to
    the `CherryPyWSGIServer` constructor.
    """
    
    from cherrypy.wsgiserver import CherryPyWSGIServer
    
    bind_addr = (config['server.bind'], config['server.port'])
    kwargs = dict(
        numthreads=config['server.num-threads'],
        server_name=config['server.name'],
        request_queue_size=config['server.request-queue-size'],
        timeout=config['server.timeout'])
    kwargs.update(extra_config)
    
    return lambda wsgi_app: CherryPyWSGIServer(bind_addr, wsgi_app, **kwargs)

Config.server_maker = server_maker
