# Configuration

All Markdoc wikis are configured via a single `markdoc.yaml` file in the wiki
root. This file is formatted with YAML (Yet Another Markup Language); you can
find more information on that at [yaml.org](http://yaml.org/). When running the
command-line interface, Markdoc will search for either a `markdoc.yaml` or a
`.markdoc.yaml` file in the current directory. You can also explicitly specify a
file to use with the `-c`/`--config` command-line option.

## Example

Here we’ll go through an example and show how the various settings affect
Markdoc’s behavior:

    #!yaml
    # Metadata
    wiki-name: "My Wiki"
    google-analytics: UA-XXXXXX-X
    
    # Directories
    hide-prefix: "."
    wiki-dir: "wiki"
    static-dir: "static"
    html-dir: ".html"
    template-dir: ".templates"
    temp-dir: ".tmp"
    cvs-exclude: true
    
    # Building
    document-extensions: [.md, .mdown, .markdown, .wiki, .text]
    generate-listing: always
    listing-filename: "_list.html"
    use-default-static: true
    use-default-templates: true
    
    # Rendering
    markdown:
      safe-mode: false
      output-format: xhtml1
      extensions: [codehilite, def_list]
      extension-configs:
        codehilite:
          force_linenos: true
    
    # Serving
    server:
      bind: '127.0.0.1'
      port: 8010
      num-threads: 10
      name: 'server.example.com'
      request-queue-size: 5
      timeout: 10

Remember that Markdoc uses sensible defaults for *all* of these options, so it’s
perfectly OK to have an empty markdoc.yaml file. You still need one though.

*   [Metadata](#metadata)
*   [Directories](#directories)
*   [Building](#building)
*   [Rendering](#rendering)
*   [Serving](#serving)

### Metadata

This is information about your wiki itself. It is currently only used when
rendering the default set of templates, but custom templates may also use these
parameters.

`wiki-name` (no default)
:   Specify the human-friendly name of your wiki. If defined, this will appear
    in the title and footer in the default Markdoc templates.

`google-analytics` (no default)
:   Specify a [Google Analytics][] tracking key for your Markdoc site. If given,
    the GA tracking code will be included in every HTML document. Note that this
    should be the full key, in the format `UA-XXXXXX-X`.

  [google analytics]: http://google.com/analytics/

### Directories

These settings affect where Markdoc looks for some pieces of data, and where it
puts others. You can get more information on the roles of various directories in
the [layout documentation](/layout). Note that all `*-dir` parameters are
resolved relative to the wiki root, and that `'.'` (i.e. the wiki root itself)
is an acceptable value.

`hide-prefix` (default `.`)
:   This determines how Markdoc finds and writes to hidden directories like
    `.tmp`, `.templates` and `.html`. You may wish to set this to `'_'` if your
    VCS or operating system doesn’t play nicely with period-prefixed filenames.
    If you specify `html-dir`, `temp-dir` and `template-dir`, this setting won’t
    have any effect.

`wiki-dir` (default `"wiki"`)
:   This tells Markdoc where to find pages that should be rendered with Markdown
    and output as HTML. Only files in this directory will be rendered.

`static-dir` (default `"static"`)
:   Any files in the static directory are synced over to the HTML root as-is
    when building. This tells Markdoc where to find all the static media for
    your wiki.

`html-dir` (default `hide-prefix + "html"`)
:   This is where HTML and static media are eventually output during the
    building process. It is also the document root for the Markdoc server. The
    default value is auto-generated using the `hide-prefix` setting.

`template-dir` (default `hide-prefix + "templates"`)
:   Markdoc will look in this directory first when searching for the Jinja2
    templates needed to produce HTML.

`temp-dir` (default `hide-prefix + "tmp"`)
:   This directory is used as a temporary destination when building HTML.

`cvs-exclude` (default `true`)
:   If this is `true`, Markdoc will pass the `--cvs-exclude` option to `rsync`
    when syncing static media and rendered HTML files. This causes `rsync` to
    skip some common backup/hidden files (e.g. `.git/`, `.svn/`, `*~` and `#*`).
    The full semantics of this option are specified in the
    [`rsync` documentation][rsync-docs].

  [rsync-docs]: http://www.samba.org/ftp/rsync/rsync.html

### Building

These settings affect Markdoc’s behavior during the build process.

`document-extensions` (default `[.md, .mdown, .markdown, .wiki, .text]`)
:   Markdoc will only render files from the document root which have one of
    these extensions. If one of the extensions is an empty string (`''`), then
    all files (including those without an extension) will be considered pages.
    Setting this parameter to the empty list (`[]`) will behave as if it is
    actually `['']`.

`generate-listing` (default `always`)
:   This affects how listings are generated for directories in your Markdoc wiki
    (including the top level). Set this to either `always`, `sometimes` or
    `never`. The semantics are as follows:
  
    *   `never` never generates any listings.
    *   `sometimes` only generates a listing when there is no `index` or
        `index.html` file in a directory. This listing is saved as both
        `index.html` and the value of the `listing-filename` setting.
    *   `always` generates a listing for every directory, and saves it under the
        value of the `listing-filename` setting, and as `index.html` if an index
        file does not already exist.

`listing-filename` (default `_list.html`)
:   This specifies the filename that directory listings are saved under; see the
    documentation for `generate-listing` just above for more information.

`use-default-static` (default `true`)
:   If true, Markdoc’s default set of static media will be synchronized to the
    HTML root when building.

`use-default-templates` (default `true`)
:   If true, Jinja2 will look in Markdoc’s set of default templates when
    rendering documents and listings.

### Rendering

These settings determine how Markdoc converts Markdown text into XHTML. They are
all defined as sub-parameters inside the `markdown` dictionary. These parameters
correspond to keyword arguments to the `markdown.Markdown` constructor, although
hyphens (`-`) are all converted to underscores (`_`) in the key strings.

`extensions` (default `[]`)
:   A list of strings specifying extensions to be used by the Markdown renderer.
    The [Markdown library for Python][markdown-python-lib] comes with the
    following by default:
  
    * `abbr`
    * `codehilite`
    * `def_list`
    * `extra`
    * `fenced_code`
    * `footnotes`
    * `headerid`
    * `html_tidy`
    * `imagelinks`
    * `meta`
    * `rss`
    * `tables`
    * `toc`
    * `wikilinks`

  [markdown-python-lib]: http://www.freewisdom.org/projects/python-markdown

`extension-configs` (default `{}`)
:   These are configuration parameters for the extensions — you’ll need to
    consult the official Markdown library documentation for more information.

`safe-mode` (default `false`)
:   Disallow raw HTML in Markdown documents. This can be either `false`,
    `remove`, `replace` or `escape`.

`output-format` (default `xhtml1`)
:   Switch between rendering XHTML or HTML. Can be either `xhtml1`, `xhtml`,
    `html4` or `html` (the general ones will always refer to the latest
    version). It is strongly suggested that you use XHTML.

### Serving

All of the server configuration parameters exist in the `server` dictionary (as
with `markdown` previously).

`bind` (default `127.0.0.1`)
:   Bind to the specified interface. With the default value the server will only
    listen on the loopback interface (localhost).

`port` (default `8008`)
:   Listen on the specified port.

`num-threads` (default `10`)
:   Use this number of threads to handle requests.

`name` (default is autodetected)
:   Specify a server name. The default will be automatically detected from the
    socket the server binds to.

`request-queue-size` (default `5`)
:   Sets the number of queued connections to the server before it will start
    dropping TCP connections (the `backlog` argument to `socket.listen()`).

`timeout` (default `10`)
:   The socket timeout (in seconds) for accepted TCP connections.
