wpclassifier
============

A very simple tool organising wallpapers by dimensions.
It takes one input folder and one output folder as parameter.

Inside the output folder, it will create subfolders like "1024x768",
"1920x1080", ... representing the image resolutions

Alternatively, it can also produce folders representing the image
aspect ratio (for example: 4@3). It uses `@` instead of the
conventional `:` to stay compatible with windows.

The images in the input folder will be moved into the corresponding folders.


Run `wpclassifier --help` for the command-line help.