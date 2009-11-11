# Layout

Markdoc wikis have the following layout:

    WIKI_ROOT/
    |-- .html/
    |-- .templates/
    |-- .tmp/
    |-- static/
    |-- wiki/
    `-- config.yaml

The `.html/` and `.tmp/` directories should be excluded from any VCS, since they contain temporary files.

: `WIKI_ROOT/`
The root of the wiki, containing all of the files required for the `markdoc` utility to build and serve the wiki.

: `WIKI_ROOT/.html/`
Holds the compiled HTML and static files. It is directly served from by the Markdoc webserver.

: `WIKI_ROOT/.templates/`
Contains the Jinja2 templates for documents and directory listings. It comes with some sensible (and, I hope, pretty) defaults, but you can override these if you wish.

: `WIKI_ROOT/.tmp/`
Used as a temporary build destination directory for rendered Markdown files. This directory is then rsync’d to `WIKI_ROOT/.html/` along with `WIKI_ROOT/static`; the incremental nature of this operation means the server can keep running in one process whilst another runs `markdoc build`.

: `WIKI_ROOT/static/`
Static media files (such as CSS and JavaScript) should be put in this directory. They will be copied to `.html/` by rsync during the build operation. As with `.templates/`, this comes with some defaults.

: `WIKI_ROOT/wiki/`
This contains the actual *text* of your wiki, in `.md` Markdown-formatted files. It is assumed they are UTF-8 encoded. Any files without a valid extension will be ignored.

: `WIKI_ROOT/config.yaml`
This is the main configuration point for your wiki, in a YAML-formatted file. Consult the [configuration docs](/configuration) for more information.