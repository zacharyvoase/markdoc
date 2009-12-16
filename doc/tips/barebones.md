# Barebones Wikis

Out of the box, Markdoc supports relatively complex wikis with custom templates and static files. However, for many cases, the default media and templates are adequate, so why should a vanilla wiki require nesting like the following:

    :::text
    some-wiki/
    |-- .templates/
    |-- static/
    |-- wiki/
    |   |-- files
    |   |-- go
    |   `-- here
    `-- markdoc.yaml

Fortunately, for very simple cases where you just want to be able to render and serve a collection of Markdown-formatted files, you can do so. Begin by just creating and entering an empty directory:

    :::bash
    $ mkdir mywiki/
    $ cd mywiki/

Now create a file called `.markdoc.yaml` containing the following YAML data:

    :::yaml
    wiki-name: My Wiki # Set this to whatever you want
    
    wiki-dir: "."
    static-dir: ".static"

You can add some more configuration parameters if you like, but these are the basic ones you’ll need. So now your directory structure will look like this:

    :::text
    mywiki/
    `-- .markdoc.yaml

And you can just start creating pages in the directory.

    :::text
    mywiki/
    |-- .markdoc.yaml
    |-- page1.md
    |-- page2.md
    `-- page3.md

To run the build process, just do the usual:

    :::bash
    $ markdoc build && markdoc serve

`markdoc` recognizes both `markdoc.yaml` *and* `.markdoc.yaml` implicitly. Because you’ve hidden everything except the actual wiki pages, to most file browsers (including `ls`) the wiki will just look like a directory with a number of text files.
