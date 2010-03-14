# About Markdoc

Markdoc is a project which aims to provide a lightweight alternative to large
database-powered wiki systems. I’ve listed the main goals of the project below;
I believe that, in its current state, it meets all of these.


## Goals & Philosophy

### Wikis

*   Wikis should be made up of plain-text files, without requiring a running
    instance of MySQL or even an SQLite database.

*   There should only be one simple-to-write plain-text configuration file.

*   Wikis should be VCS-friendly, yet VCS-agnostic.

*   It should be possible to compile a wiki to static HTML, and then to serve
    this HTML with no wiki-specific software.


### Markdown

I chose Markdown as the format for this wiki system because of its simplicity,
familiarity for many writers, and the extensibility of its Python
implementation. For example, Pygments syntax highlighting is available through a
single configuration option in the `markdoc.yaml` file. The ability to embed raw
HTML in Markdown documents gives it power and flexibility.


### Command-Line Interface

*   The CLI should be intuitive and easy to use.

*   There should only be a few different sub-commands, each of which does what
    one would expect it to.

*   There should be a full web server included, in the case that setting up a
    large-scale HTTP server is impractical or impossible.

*   The CLI should be pure-Python, for portability and extensibility.


## License

Markdoc is [public domain software](http://unlicense.org/).

> This is free and unencumbered software released into the public domain.
> 
> Anyone is free to copy, modify, publish, use, compile, sell, or distribute
> this software, either in source code form or as a compiled binary, for any
> purpose, commercial or non-commercial, and by any means.
> 
> In jurisdictions that recognize copyright laws, the author or authors of this
> software dedicate any and all copyright interest in the software to the public
> domain. We make this dedication for the benefit of the public at large and to
> the detriment of our heirs and successors. We intend this dedication to be an
> overt act of relinquishment in perpetuity of all present and future rights to
> this software under copyright law.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
> ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
> WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
> 
> For more information, please refer to <http://unlicense.org/>


The bundled Pygments style (it’s the [Github][] syntax highlighting theme) was
created by [Tom Preston-Werner][]; it was sourced from [his blog][] and is
licensed under the MIT License:

  [github]: http://github.com/
  [tom preston-werner]: http://tom.preston-werner.com/
  [his blog]: http://github.com/mojombo/tpw/

> Copyright © 2010 Tom Preston-Werner
> 
> Permission is hereby granted, free of charge, to any person
> obtaining a copy of this software and associated documentation
> files (the "Software"), to deal in the Software without
> restriction, including without limitation the rights to use,
> copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following
> conditions:
> 
> The above copyright notice and this permission notice shall be
> included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
> OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
> NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
> HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
> FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.