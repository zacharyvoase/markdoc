# Configuration

All Markdoc wikis are configured via a single `markdoc.yaml` file in the wiki root. This file is formatted with YAML (Yet Another Markup Language); you can find more information on that at [yaml.org](http://yaml.org/).

## Example

Here we’ll go through an example and show how the various settings affect Markdoc’s behavior:

    #!yaml
    hide-prefix: "."
    document-extensions: [.md, .mdown, .markdown, .wiki, .text]
    generate-listing: always
    listing-filename: "_list.html"
    use-default-static: true
    use-default-templates: true
    
    markdown:
      safe_mode: false
      output_format: xhtml1
      extensions: [codehilite, def_list]
      extension_configs:
        codehilite:
          force_linenos: true
    
    server:
      bind: '127.0.0.1'
      port: 8010
      server_name: 'server.example.com'

Remember that Markdoc uses sensible defaults for *all* of these options, so it’s perfectly OK to have an empty markdoc.yaml file. You still need one though.

`hide-prefix` (default `.`)
: This determines how Markdoc finds and writes to hidden directories like `.tmp`, `.templates` and `.html`. You may wish to set this to `'_'` if your VCS or operating system doesn’t play nicely with period-prefixed filenames.

`document-extensions` (default `[.md, .mdown, .markdown, .wiki, .text]`)
: Markdoc will only render files from the document root which have one of these extensions.

`generate-listing` (default `always`)
: This affects how listings are generated for directories in your Markdoc wiki (including the top level). Set this to either `always`, `sometimes` or `never`. The semantics are as follows:
  
  * `never` never generates any listings.
  * `sometimes` only generates a listing when there is no `index` or `index.html` file in a directory. This listing is saved as both `index.html` and the value of the `listing-filename` setting.
  * `always` generates a listing for every directory, and saves it under the value of the `listing-filename` setting, and as `index.html` if an index file does not already exist.

`listing-filename` (default `_list.html`)
: This specifies the filename that directory listings are saved under; see the documentation for `generate-listing` just above for more information.

`use-default-static` (default `true`)
: If true, Markdoc’s default set of static media will be synchronized to the HTML root when building.

`use-default-templates` (default `true`)
: If true, Jinja2 will look in Markdoc’s set of default templates when rendering documents and listings.

`markdown` (default is empty)
: This should hold a dictionary with keyword arguments for the `markdown.Markdown` constructor. You can see an example above; also try consulting the Python Markdown library documentation to see what values can be given here.

`server`
: This specifies how to serve the wiki, as wiki-specific defaults for the `markdoc serve` command. Consult `markdoc serve --help` for a list of configuration parameters; just remember that `--long-option` will map out to a key of `long_option` in this dictionary.
