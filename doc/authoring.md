# Authoring

A wiki would be nothing without pages. In Markdoc, pages are written in
[Markdown][df-markdown], a plain-text formatting syntax designed by
[John Gruber][df]. In his own words:

  [df]: http://daringfireball.net/
  [df-markdown]: http://daringfireball.net/projects/markdown/

> Markdown allows you to write using an easy-to-read, easy-to-write plain text 
> format, then convert it to structurally valid XHTML (or HTML).
> 
> [...]
> 
> The overriding design goal for Markdown’s formatting syntax is to
> make it as readable as possible. The idea is that a Markdown-formatted
> document should be publishable as-is, as plain text, without looking
> like it’s been marked up with tags or formatting instructions.

For a comprehensive guide to the Markdown syntax, consult the
[markup reference documentation](/ref/markup). The rest of this document will
cover the Markdoc-specific conventions and constraints related to writing wiki
pages.


## Linking

Every page in your wiki will likely link to several other pages. Markdoc does
not require any special syntax for internal links; the usual Markdown format
will work. An example of a link from this very page follows:

    :::text
    For a comprehensive guide to the Markdown syntax,
    consult the [markup reference documentation](/ref/markup).

As you can see, the link href is an absolute path to the document, without any
extension. Markdoc will process this and convert it into a relative path when
rendering the corresponding HTML. This means that you can host Markdoc wikis
under sub-directories on a web server, and the links will still work properly.

If you split your wiki up into sub-directories (for example, in this wiki, there
is an `internals/` directory), the pattern remains the same. A link to the
[internals/rendering](/internals/rendering) document looks like this:

    :::text
    A link to the [internals/rendering](/internals/rendering) document.

Note that links will only be made relative if they begin with a `/` character;
for example, a link to `http://www.google.com/` will be left untouched.
