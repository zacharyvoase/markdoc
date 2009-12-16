# Syntax Highlighting with Pygments

[Markdown for Python][] supports syntax highlighting in your documents using [Pygments][]. Here’s how to set up and use it from Markdoc.

  [markdown for python]: http://www.freewisdom.org/projects/python-markdown
  [pygments]: http://pygments.org/

First, install the extension in your `markdoc.yaml` file:

    :::yaml
    wiki-name: My Wiki
    ## ...other settings...
    markdown:
      extensions:
        - codehilite # the important bit

Pygments should have been installed as a dependency when you installed Markdoc.

Initially, syntax highlighting will be applied to every code block Markdown encounters. Pygments will guess which lexer to apply to each block. To specify the language of a block, add a `:::LANG` prefix to blocks of code. For example:

    :::text
    :::python
    def hello():
        print "Hello, World!"

Will render to:

    :::python
    def hello():
        print "Hello, World!"

To switch syntax highlighting off for a block, use `:::text`.

If you want a block to have line numbers, use `#!LANG` instead. For example:

    :::text
    #!ruby
    class Foo
      def bar
        @baz
      end
    end

Will render to:

    #!ruby
    class Foo
      def bar
        @baz
      end
    end

If you add a shebang to a code block, like `#!/bin/bash` or `#!/usr/bin/env python`, the language will be guessed and the shebang included in the output. In the final text. So for example, the following:

    :::text
    #!/bin/bash
    echo "Hello, World"

Will render to:

    #!/bin/bash
    echo "Hello, World"
