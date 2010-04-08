# Development

Markdoc is actively developed via [GitHub][gh-markdoc].

  [gh-markdoc]: http://github.com/zacharyvoase/markdoc

## Working with the Repository

You’ll need to install [Git][git] first; check your OS’s package manager for a
`git` or `git-core` package.

  [git]: http://git-scm.com/

You can check out a copy of the repository by cloning it:

    :::bash
    $ git clone git://github.com/zacharyvoase/markdoc.git
    $ cd markdoc/

### Repo Structure

There are several files and directories in the root of the repo:

    :::text
    markdoc/
    |-- doc/
    |-- src/
    |-- test/
    |-- UNLICENSE
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

`UNLICENSE`
:   The text of the unlicense which designates Markdoc as public domain software.

`MANIFEST.in`, `setup.py`, `distribute_setup.py`
:   The necessary Python packaging machinery, so you can run
    `easy_install Markdoc`.

`README`
:   Doesn’t need an explanation.

`REQUIREMENTS`
:   A text file listing all of Markdoc’s requirements, suitable for use with
    `pip install -r REQUIREMENTS`. [pip][] is a next-generation `easy_install` 
    replacement for Python.


  [pip]: http://pip.openplans.org/
  [nose]: http://somethingaboutorange.com/mrl/projects/nose/0.11.1/

### Bug Reporting and Feature Requests

All bugs and feature requests are handled on the [GitHub issues page](http://github.com/zacharyvoase/markdoc/issues).

### Contributing

If you’re interested in implementing a feature or extension for Markdoc, just fork the GitHub repository, work on the feature, commit your changes, then send me a pull request. If I like what you’ve done, I’ll pull your changes into the official Markdoc release and give you author credit.

Remember that you must be willing to release your changes to the public domain. If you are submitting a non-trivial patch, take a look at [unlicense.org][unlicensing contributions] for detailed instructions; for now, you just need to agree to the following statement:

  [unlicensing contributions]: http://unlicense.org/#unlicensing-contributions

    :::text
    I dedicate any and all copyright interest in this software to the
    public domain. I make this dedication for the benefit of the public at
    large and to the detriment of my heirs and successors. I intend this
    dedication to be an overt act of relinquishment in perpetuity of all
    present and future rights to this software under copyright law.
