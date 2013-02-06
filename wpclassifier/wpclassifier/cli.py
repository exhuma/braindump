import sys
import logging
from optparse import OptionParser, IndentedHelpFormatter

from wpclassifier import (
        move_files,
        aspect_folder,
        F_APPROX_ASPECT,
        F_SIMPLE,
        F_ASPECT)

LOG = logging.getLogger(__name__)


class MyHelpFormatter(IndentedHelpFormatter):

    def format_epilog(self, eplg):
        return eplg


def main():

    usage = "%prog [options] <input_dir> <output_dir>"
    parser = OptionParser(usage=usage, formatter=MyHelpFormatter())
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help="Be more verbose")
    parser.add_option('-m', '--move', dest='move', action='store_true',
            default=False, help="Instead of copying the files, the files "
            "will be moved to the destination. Default=False")
    parser.add_option('-f', '--format', dest='format', default=F_SIMPLE,
            help='Target folder format. Can be one of {0}, {1} or {2}'.format(
                   F_SIMPLE,
                   F_ASPECT,
                   F_APPROX_ASPECT))
    parser.add_option('-s', '--target-for', dest='target_for',
            metavar='SIZE', default=None,
            help='Show the target folder for a given resolution '
                 'and exit. For example: SIZE=1680x1050')
    epilog = """\

FORMATS
=======

There are three different naming options for target folders:

--format=s (the default)
    When using this format, the application will simply generate folders
    representing width and height. An image with a width of 1920 and height op
    1080 will be saved to a folder named '1920x1080'.

--format=a
    This will store the images into folders which represent the images aspect
    ratio. Note that the aspect ratios will be aggressively reduced if
    possible. So an aspect ratio of "16:10" will be saved to "8@5".
    Additionally, while a proper display would be "16:9", the folder names
    will be named "16@9" for compatibility with Windows.

--format=x
    This is the same as ``--format=a`` with the difference that the
    denominator will never be larger than 10. This results in an approximate
    destination for files. So the folder "16@9" might contain images which do
    not quite have this aspect ratio. But it will always be close.
"""
    parser.epilog = epilog

    (options, args) = parser.parse_args()

    if options.target_for:
        tw, th = options.target_for.split('x')
        target = aspect_folder(int(tw), int(th), options.format)
        print "Pictures of size %s will be moved into %s" % (
                options.target_for, target)
        sys.exit(0)

    if len(args) != 2:
        parser.print_help()
        sys.exit(9)

    if options.verbose:
        print "Being verbose"
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    input_dir, output_dir = args

    move_files(input_dir, output_dir, options.format, move=options.move)
