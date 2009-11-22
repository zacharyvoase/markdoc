# Quickstart

Markdoc uses distutils, so you can install it with relative ease on any system with Python.

## Requirements

The minimum requirements to run the Markdoc utility are:

  * Python 2.4 or later (2.5+ highly recommended)
  * A UNIX (or at least POSIX-compliant) operating system
  * [pip](http://pip.openplans.org/) (you can get it via `easy_install -U pip`)
  * [rsync](http://www.samba.org/rsync/) -- installed out of the box with most modern OSes, including Mac OS X and Ubuntu. In the future Markdoc may include a pure-Python implementation.

`pip` is used to install all of the Python dependencies, which are individually listed in the `REQUIREMENTS` file alongside this README. If you don't want to use `pip`, you can manually go through this list and run `easy_install <package>` on each package name.

## Installation

    #!bash
    $ hg clone ssh://hg@bitbucket.org/zacharyvoase/markdoc
    $ cd markdoc/
    $ pip install -r REQUIREMENTS # Or your preferred method.
    $ python setup.py install

## Making a Wiki

### Initializing the Wiki

The `markdoc init` command creates a new wiki. It also accepts a `--vcs-ignore` option which will automatically create the appropriate ignore file for your VCS.

    #!bash
    $ markdoc init my-wiki --vcs-ignore hg
    --> markdoc init
    # ...logging output...

### Editing Pages

Documents in a Markdoc wiki are located under the `wiki/` subdirectory, and are plain Markdown files. Typically documents have a `.md` file extension, but in the [wiki configuration](/configuration#building) you can specify others.

    $ cd my-wiki/
    $ vim wiki/somefile.md
    # ... write some documents ...

### Building

Markdoc comes with a default set of templates and stylesheets, so you can build your wiki right away. Just run `markdoc build`, and all the HTML will be generated and output into the `.html/` sub-directory (known as the HTML root).

    $ markdoc build
    --> markdoc build
    # ...more logging output...

### Serving

You can view all the HTML in a browser easily by running the built-in server. `markdoc serve` accepts a large number of options, but on its own will serve your documentation on port 8008.

    $ markdoc serve
    --> markdoc serve
    # ...even more logging output...

Now just open <http://localhost:8008/> in your browser, and see your new Markdoc-powered wiki!
