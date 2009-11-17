# Quickstart

Markdoc is not yet available as an `easy_install`-able package, but it does use distutils so you can install it with relative ease on any system with Python.

## Requirements

The minimum requirements to run the Markdoc utility are:

  * Python 2.4 or later (2.5+ highly recommended)
  * A UNIX (or at least POSIX-compliant) operating system
  * [pip](http://pip.openplans.org/) (you can get it via `easy_install -U pip`)
  * [rsync](http://www.samba.org/rsync/) -- installed out of the box with most
    modern OSes, including Mac OS X and Ubuntu. In the future Markdoc may
    include a pure-Python implementation.

`pip` is used to install all of the Python dependencies, which are individually
listed in the `REQUIREMENTS` file alongside this README. If you don't want to
use `pip`, you can manually go through this list and run
`easy_install <package>` on each package name.

## Installation

    #!bash
    $ hg clone ssh://hg@bitbucket.org/zacharyvoase/markdoc
    $ cd markdoc/
    $ pip install -r REQUIREMENTS # Or your preferred method.
    $ python setup.py install

## Making a Wiki
    
    #!bash
    $ markdoc init my-wiki
    --> markdoc init
    # ...logging output...
    $ cd my-wiki/
    $ vim wiki/somefile.md
    # ... write some documentation ...
    $ markdoc build
    --> markdoc build
    # ...more logging output...
    $ markdoc serve
    --> markdoc serve
    # ...even more logging output...

Now just open <http://localhost:8008/> in your browser, and see your new Markdoc-powered wiki!
