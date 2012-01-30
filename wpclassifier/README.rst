wpclassifier
============

A very simple tool organising wallpapers by dimensions.
It takes one input folder and one output folder as parameter.

Inside the output folder, it will create subfolders like "1024x768",
"1920x1080", ... representing the image resolutions

Alternatively, it can also produce folders representing the image
aspect ratio (for example: 4@3). It uses ``@`` instead of the
conventional ``:`` to stay compatible with windows.

The images in the input folder will be moved into the corresponding folders.


Run ``wpclassifier --help`` for the command-line help.

Installation
============

You can install the package either by using ``pip`` or the default
``python`` interpreter. It is also possible to install it into a
``virtualenv``.

The respective commans are::

    [/path/to/virtualenv/bin/]python setup.py install

or::

   pip install [-E /path/to/virtualenv] -e .

Dependencies will automatically fetched as needed.

.. note:: On windows the dependency resolution may fail if you have
          no C compiler installed. In this case, look into the
          ``setup.py`` file to locate the dependencies and download
          and install these packages manually.

The main executable will be placed in the proper place
(``/usr/local/bin``, ``/path/to/virtualenv/bin``,
``C:\Python\scripts``) automatically.