# -*- coding: utf-8 -*-

import logging
import mimetypes
import os.path as p

import webob

from markdoc.render import make_relative


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
        self.log = logging.getLogger('markdoc.wsgi')
    
    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        response = self.get_response(request)
        self.log.info('%s %s - %d' % (request.method, request.path_info, response.status_int))
        return response(environ, start_response)
    
    def is_safe(self, directory):
        """Make sure the given absolute path does not point above the htroot."""
        
        return p.pardir not in p.relpath(directory, start=self.config.html_dir).split(p.sep)
    
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
        * If a file of the same name with a 'html' extension exists in the
          parent directory, redirect to it (without the trailing slash); else
        * Return a HTTP 404 ‘Not Found’.
        """
        
        path_parts = request.path_info.strip('/').split('/')
        index_filename = p.join(self.config.html_dir, *(path_parts + ['index.html']))
        if p.exists(index_filename) and self.is_safe(index_filename):
            return serve_file(index_filename)
        
        directory_filename = p.join(self.config.html_dir, *path_parts)
        if p.isfile(directory_filename) or p.isfile(directory_filename + p.extsep + 'html'):
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
        
        path_parts = request.path_info.strip('/').split('/')
        filename = p.abspath(p.join(self.config.html_dir, *path_parts))
        if not self.is_safe(filename):
            return self.forbidden(request)
        
        if p.isfile(filename):
            pass
        elif p.isfile(filename + p.extsep + 'html'):
            filename = filename + p.extsep + 'html'
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
        
        Note that the templating machinery is only invoked when the browser is
        expecting HTML. This is determined by calling
        `request.accept.accept_html()`. If not, an empty response (i.e. one
        without a content body) is returned.
        """
        
        response = webob.Response()
        response.status = status
        
        if request.accept.accept_html():
            context = {}
            context['request'] = request
            context['is_index'] = request.path_info in ['/', '/index.html']
            context['make_relative'] = lambda href: make_relative(request.path_info, href)
            context['status'] = status
            context['reason'] = webob.statusreasons.status_reasons[status]
            
            template = self.config.template_env.get_template('%d.html' % status)
            response.unicode_body = template.render(context)
            response.content_type = mimetypes.types_map['.xhtml']
        else:
            del response.content_length
            del response.content_type
        
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
    
    if content_type.startswith('text/html'):
        content_type = content_type.replace('text/html', 'application/xhtml+xml')
    
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
