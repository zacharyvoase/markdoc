# Development

Markdoc is actively developed through its [Bitbucket page][bb-markdoc]. The [Mercurial Version Control System][hg] is used to manage the software history

  [bb-markdoc]: http://bitbucket.org/zacharyvoase/markdoc

## Working with the Repository

You’ll need to install [Mercurial][hg] first; check your OS’s package manager for a `mercurial` or `hg` package.

You can check out a copy of the repository by cloning it:

    :::bash
    $ hg clone http://bitbucket.org/zacharyvoase/markdoc
    $ cd markdoc/

### Repo Structure

There are several files and directories in the root of the repo:

    :::text
    markdoc/
    |-- doc/
    |-- src/
    |-- test/
    |-- LICENSE
    |-- MANIFEST.in
    |-- README
    |-- REQUIREMENTS
    |-- distribute_setup.py
    |-- nose.cfg
    `-- setup.py

`doc/`
:   A Markdoc wiki containing Markdoc’s own documentation. How very meta.

`src/`
:   The home of all of Markdoc’s Python code.

`test/`, `nose.cfg`
:   Markdoc’s tests (Python + Doctests) and nose configuration. [Nose][] is a 
    Python utility to automate and simplify running complex test suites.

`LICENSE`
:   The text of the MIT/X11 license under which Markdoc is released.

`MANIFEST.in`, `setup.py`, `distribute_setup.py`
:   The necessary Python packaging machinery, so you can run
    `easy_install Markdoc`.

`README`
:   Doesn’t need an explanation.

`REQUIREMENTS`
:   A text file listing all of Markdoc’s requirements, suitable for use with
    `pip install -r REQUIREMENTS`. [pip][] is a next-generation `easy_install` 
    replacement for Python.


  [hg]: http://mercurial.selenic.com/
  [pip]: http://pip.openplans.org/
  [nose]: http://somethingaboutorange.com/mrl/projects/nose/0.11.1/

### Bug Reporting and Feature Requests

All bugs and feature requests are handled on the [Bitbucket issues page](http://bitbucket.org/zacharyvoase/markdoc/issues/).

### Contributing

If you’re interested in implementing a feature or extension for Markdoc, just fork the Bitbucket repository, work on the feature, commit your changes, then send me a pull request. If I like what you’ve done, I’ll pull your changes into the official Markdoc release and give you author credit. Note: you must be willing to release your changes under Markdoc’s [license][], which is a standard MIT/X11 license.

  [license]: http://bitbucket.org/zacharyvoase/markdoc/src/tip/LICENSE
