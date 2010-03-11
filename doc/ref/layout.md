# Layout

Markdoc wikis have the following layout:

    :::text
    WIKI_ROOT/
    |-- .html/
    |-- .templates/
    |-- .tmp/
    |-- static/
    |-- wiki/
    `-- markdoc.yaml

The `.html/` and `.tmp/` directories should be excluded from any VCS, since they
contain temporary files. Here is a list of the roles of the various files and
sub-directories, in descending order of significance:

`WIKI_ROOT/`
:   The *wiki root*, containing all of the files required for the `markdoc`
    utility to build and serve the wiki.

`WIKI_ROOT/markdoc.yaml`
:   The *wiki configuration*; the main configuration point for your wiki, in a
    YAML-formatted file. Consult the [configuration docs](/configuration) for
    more information on how to write this.

`WIKI_ROOT/wiki/`
:   The *document root*, which contains the actual *text* of your wiki in
    Markdown-formatted text files. It is assumed they are UTF-8 encoded. Any
    files without a valid extension will be ignored (see the option
    `document-extensions` in [configuration](/configuration)).

`WIKI_ROOT/static/`
:   The *static directory*: static media files (such as CSS and JavaScript)
    should be put here. They will be copied to `.html/` by rsync during the
    build operation. This comes with some default CSS for styling.

`WIKI_ROOT/.templates/`
:   The *template directory*: it contains the Jinja2 templates for documents,
    error pages and directory listings. It comes with some nice defaults, but
    you can override these if you wish.

`WIKI_ROOT/.html/`
:   The *HTML root* (sometimes abbreviated as ‘htroot’). It holds the compiled
    HTML and static files. It is directly served from by the Markdoc webserver.

`WIKI_ROOT/.tmp/`
:   The *temporary directory*: a temporary build destination for rendered
    Markdown files. This directory is then rsync’d to the HTML root along with
    the static directory; the incremental nature of this operation means the
    Markdoc web server can keep running in one process whilst another runs
    `markdoc build`.

Note that all of the default locations for these directories can be overridden
in the `markdoc.yaml` file. For example, you may wish to use `WIKI_ROOT/pages/`
instead of `WIKI_ROOT/wiki/`, or `WIKI_ROOT/.build/` instead of
`WIKI_ROOT/.html/`. Consult the [configuration documentation](/configuration)
for more information.
