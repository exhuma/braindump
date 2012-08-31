#!/usr/bin/python
"""
*Very* simple tool to pretty-print JSON data.

It's primary use is to pipe in the output of ``curl``. For example::

   curl -H "Accept: application/json" -X GET http://url/ | jsonf

or, with headers::

   curl -i -H "Accept: application/json" -X GET http://url/ | jsonf

Handling headers is *very* curl specific and not tested with any other source.
Given that curl's output looks like a standard HTTP response, it should work
with other tools too. YMMV.
"""
from sys import stdin, stderr
import json

try:
    from pygments import highlight
    from pygments.lexers import JSONLexer
    from pygments.formatters import TerminalFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


def format_json(data):
    return json.dumps(json.loads(data), sort_keys=True, indent=4)


def main():
    headers = []
    content = []
    active_list = headers
    headers_done = False
    for line in stdin:
        if not headers_done and not line.strip():
            active_list = content
            continue
        active_list.append(line)

    if not content:
        # no headers found, so the content had been loaded in the wrong list.
        # Let's exchange them.
        content, headers = headers, content

    print ''.join(headers)
    output = format_json(''.join(content))
    if PYGMENTS_AVAILABLE:
        print highlight(output, JSONLexer(), TerminalFormatter())
    else:
        print output
        print >>stderr, ("NOTE: If you have the python package "
                         "`pygments` available for import, you'll get nice "
                         "syntax highlighting ^_^")


if __name__ == '__main__':
    main()
