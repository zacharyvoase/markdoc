# About Markdoc

Markdoc is a project which aims to provide a lightweight alternative to large database-powered wiki systems. Below I have included the main goals and philosophy of the Markdoc project; I believe Markdoc currently meets all of these.

## Goals & Philosophy

### Wikis

* Wikis should be made up of plain-text files, without requiring a running instance of MySQL or even an SQLite database.

* There should only be one simple-to-write plain-text configuration file.

* Wikis should be VCS-friendly, yet VCS-agnostic.

* It should be possible to compile a wiki to static HTML, and then to serve this HTML with no wiki-specific software.

### Markdown

I chose Markdown as the format for this wiki system because of its simplicity, familiarity for many writers, and the extensibility of its Python implementation. For example, Pygments syntax highlighting is available through a single configuration option in the `markdoc.yaml` file. The ability to embed raw HTML in Markdown documents gives it power and flexibility.

### Command-Line Interface

* The CLI should be intuitive and easy to use.

* There should only be a few different sub-commands, each of which does what one would expect it to.

* There should be a full web server included, in the case that setting up a large-scale HTTP server is impractical or impossible.

* The CLI should be pure-Python, for portability and extensibility.
