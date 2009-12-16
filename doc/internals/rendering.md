# Rendering

This page will describe the process which documents undergo on their way from Markdoc to XHTML.

## Step 1: Markdown Rendering

Each page is converted from Markdown to XHTML. This uses the Markdown library for Python, which comes with a number of extensions that you can enable in your [configuration](/configuration). For example, I like to use the `codehilite`, `def_list` and `headerid` Markdown extensions, but by default Markdoc wikis will not use any.

The Markdown conversion results in XHTML data which is not tied to a page, so it’s not enough to display to a browser. That’s where the templating comes in.

## Step 2: Template Rendering

Markdoc uses [Jinja2][] to render this partial XHTML to full XHTML documents. Jinja2 is a fast and flexible templating system for Python; if you are interested in writing your own templates, it would be wise to first consult its official documentation.

  [jinja2]: http://jinja2.pocoo.org

Markdoc expects only two templates to be defined: `document.html` and `listing.html`. The way it finds these is as follows:

* It first looks for them in the `.templates/` directory inside your wiki.
* If the `use-default-templates` setting is `true` for your configuration (which it is by default), then search in the `default-templates` directory bundled with Markdoc.

If `use-default-templates` is `false` and the templates are not defined in your wiki’s template directory, Markdoc will eventually raise an error.

### Documents

`document.html` is used to convert the partial XHTML for a Markdown document into full, browser-ready XHTML. It receives a context much like the following:

    :::python
    {
      "content": "<h1>...", # The XHTML for the document.
      "title": "Some Document", # The extracted title of the document.
      "crumbs": [("index", "/"), ("some-document", None)] # Breadcrumbs
    }

The `config` variable is also (globally) set to the configuration dictionary for the current wiki.

Take a look inside the `src/markdoc/static/default-templates/markdoc-default/` directory for examples of complete templates.

### Listings

`listing.html` is used to generate listings for directories. This will only be used if `generate-listing` is set to either `always` or `sometimes` in the configuration (by default it is `always`).

Listings are a little more complex to do, so they are generated after the complete set of documents have been rendered and synced (along with static media) to the HTML root. This means you get complete listings for all of your directories, including those which came from static media.

The `listing.html` template is passed a context like this:

    :::python
    {"directory": "somedir",
     "crumbs": [("index", "/"),
                ("somedir", "/somedir/"),
                (jinja2.Markup('<span class="list-crumb">list</span>'), None)],
     "files": [{"basename": "example.css",
                "href": "/example.css",
                "humansize": "27B",
                "size": 27,
                "slug": "example"}],
     "pages": [{"basename": "hello.html",
                "href": "/subdir/hello",
                "humansize": "268B",
                "size": 268,
                "slug": "hello",
                "title": u"Hello again."}],
     "sub_directories": [{"basename": "subdir", "href": "/subdir/"}]}

The distinction between *files* and *pages* is useful because you can display links to pages with their full titles; if you’re viewing this now in a browser, just head to [/_list](/_list) to see what I mean. The filename which the list is output to can be configured with the `listing-filename` setting; this defaults to `_list.html` (hence `/_list`). You can also try `/media/_list`, et cetera.

The last crumb is special in that it displays the string `"list"` but with a class of `list-crumb`; in the default templates and media this is displayed in a light grey to indicate that it is a special page.

The semantics of listing generation are determined by the `generate-listing` setting; `always` will always generate a listing (even if it clobbers an existing file called `_list.html`), `sometimes` will only generate a listing when there is no `index.html` file for a directory, and `never` will never generate listings.

## Relative Links

For portability, all URLs pointing to files and pages within the current Markdoc wiki should be relative. This allows built wiki HTML to be hosted under a sub-directory and still maintain link integrity.

In practice, this is achieved in two parts:

*   A Markdown extension which causes absolute path URLs in links (such as
    `/path/to/somefile`) to be converted to relative ones (like `../somefile`).

*   A callable passed to every template context which, when called with an
    absolute path URL, will convert it to a relative one. This variable is
    `make_relative()`, and an example of its use can be seen in this snippet
    from the default base template:
        
        :::text
        <head>
          <!--...snip...-->
          
          {% import "macros/html" as html -%}
          
          {{ html.cssimport(make_relative("/media/css/reset.css")) }}
          {{ html.cssimport(make_relative("/media/css/layout.css")) }}
          {{ html.cssimport(make_relative("/media/css/typography.css")) }}
          {{ html.cssimport(make_relative("/media/css/pygments.css")) }}
        </head>
    
    If you override the default templates, make sure to use this callable to  
    relativize the media URLs and breadcrumb links.
