Description
===========

A simple console JSON formatter.


Reads any JSON from stdin and returns a pretty printed conversion to stdout.

Installation
============

.. note::
    This package should be fully compatible with ``virtualenv``

You can install directly using ``pip`` or ``easy_install``::

    pip install jsonf

or, respectively::

    easy_install jsonf

Installation from source
------------------------

- Download the source tarball from http://pypi.python.org/pypi or
  https://github.com/exhuma/braindump/tree/master/jsonformat

- Untar the file::

        tar xf jsonf-1.0.tar.gz

- Install it::

        cd jsonf-1.0 && python setup.py install

Usage examples
--------------

::

        echo '{ "foo" : "lorem", "bar" : "ipsum" }' | jsonf

Result::

        {
            "bar": "ipsum", 
            "foo": "lorem"
        }
