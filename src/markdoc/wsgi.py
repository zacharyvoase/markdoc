# -*- coding: utf-8 -*-

import mimetypes
import os.path as p

import webob


if not mimetypes.inited:
    mimetypes.init()
# Assume all HTML files are XHTML.
mimetypes.types_map['.html'] = mimetypes.types_map['.xhtml']


class MarkdocWSGIApplication(object):
    
    """
    A WSGI application which will serve up a Markdoc wiki.
    
    Note that this application is not specifically reserved for Markdoc wikis,
    but was designed especially for them. The handling of requests is simple,
    and is based on the request path:
    
        /[a/b/.../c/]filename
        * If the file exists relative to the docroot, serve it; else
        * If the filename with the extension 'html' exists relative to the
          docroot, serve it; else
        * If a directory exists with that name, return a redirect to it (with a
          trailing slash); else
        * Return a HTTP 404 ‘Not Found’.
        
        /[a/b/.../c/]directory/ (including the index, '/')
        * If the directory exists, look for an 'index.html' file inside it, and
          serve it if it exists; else
        * If a file of the same name exists in the parent directory, return a
          redirect to it (without the trailing slash); else
        * Return a HTTP 404 ‘Not Found’.
    
    In the context of Markdoc, if a directory does not contain an 'index.md'
    file, a listing will be generated and saved as the 'index.html' file for
    that directory.
    """
    
    def __init__(self, config):
        self.config = config
    
    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        response = self.get_response(request)
        return response(environ, start_response)
    
    @property
    def htroot(self):
        hide_prefix = self.config.setdefault('hide-prefix', '.')
        return p.join(self.config['meta']['root'], hide_prefix + 'html')
    
    def is_safe(self, directory):
        """Make sure the given absolute path does not point above the htroot."""
        
        return p.pardir not in p.relpath(directory, start=self.htroot)
    
    def get_response(self, request):
        if request.path_info.endswith('/'):
            return self.directory(request)
        return self.file(request)
    
    def directory(self, request):
        
        """
        Serve a request which points to a directory.
        
        * If the directory exists, look for an 'index.html' file inside it, and
          serve it if it exists; else
        * If a file of the same name exists in the parent directory, return a
          redirect to it (without the trailing slash); else
        * Return a HTTP 404 ‘Not Found’.
        """
        
        index_filename = p.join(self.htroot, request.path_info.lstrip('/'), 'index.html')
        if p.exists(index_filename):
            return serve_file(index_filename)
        
        directory_filename = p.join(self.htroot, request.path_info.strip('/'))
        if p.isfile(directory_filename):
            return temp_redirect(request.path_info.rstrip('/'))
        
        return self.not_found(request)
    
    def file(self, request):
        
        """
        Serve a request which points to a file.
        
        * If the file exists relative to the docroot, serve it; else
        * If the filename with the extension 'html' exists relative to the
          docroot, serve it; else
        * If a directory exists with that name, return a redirect to it (with a
          trailing slash); else
        * Return a HTTP 404 ‘Not Found’.
        """
        
        filename = p.abspath(p.join(self.htroot, request.path_info.lstrip('/')))
        if not self.is_safe(filename):
            return self.forbidden(request)
        
        if p.isfile(filename):
            pass
        elif p.isfile(filename + '.html'):
            filename = filename + '.html'
        else:
            if p.isdir(filename):
                return temp_redirect(request.path_info + '/')
            return self.not_found(request)
        
        return serve_file(filename)
    
    def error(self, request, status):
        
        """
        Serve a page for a given HTTP error.
        
        This works by rendering a template based on the HTTP error code; so an
        error of '404 Not Found' will render the '404.html' template. The
        context passed to the template is as follows:
        
        `request`
        : The `webob.Request` object for this HTTP request.
        
        `is_index`
        : A boolean indicating whether or not this is the index page. This may
        be useful in error pages where you want to link back to the home page;
        such a link will be useless in the index.
        
        `status`
        : An integer representing the HTTP status code of this error.
        
        `reason`
        : A string of the HTTP status 'reason', such as 'Not Found' for 404.
        
        The template is assumed to be valid XHTML.
        """
        
        context = {}
        context['request'] = request
        context['is_index'] = request.path_info in ['/', '/index.html']
        context['status'] = status
        context['reason'] = webob.status_reasons[status]
        
        response = webob.Response()
        response.status = status
        template = self.config.template_env.get_template('%d.html' % status)
        response.unicode_body = template.render(context)
        response.content_type = mimetypes.types_map['.xhtml']
        return response
    
    forbidden = lambda self, request: self.error(request, 403)
    not_found = lambda self, request: self.error(request, 404)


def redirect(location, permanent=False):
    """Issue an optionally-permanent redirect to another location."""
    
    response = webob.Response()
    response.status = 301 if permanent else 302
    response.location = location
    
    del response.content_type
    del response.content_length
    
    return response

temp_redirect = lambda location: redirect(location, permanent=False)
perm_redirect = lambda location: redirect(location, permanent=True)


def serve_file(filename, content_type=None, chunk_size=4096):
    
    """
    Serve the specified file as a chunked response.
    
    Return a `webob.Response` instance which will serve up the file in chunks,
    as specified by the `chunk_size` parameter (default 4KB).
    
    You can also specify a content type with the `content_type` keyword
    argument. If you do not, the content type will be inferred from the
    filename; so 'index.html' will be interpreted as 'application/xhtml+xml',
    'file.mp3' as 'audio/mpeg', et cetera. If none can be guessed, the content
    type will be reported as 'application/octet-stream'.
    """
    
    if content_type is None:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    def chunked_read(chunk_size=4096):
        fp = open(filename, 'rb')
        try:
            data = fp.read(chunk_size)
            while data:
                yield data
                data = fp.read(chunk_size)
        finally:
            fp.close()
    
    response = webob.Response(content_type=content_type)
    response.app_iter = chunked_read()
    response.content_length = p.getsize(filename)
    return response
