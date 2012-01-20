import sys
import logging
from optparse import OptionParser

from wpclassifier import move_files

LOG = logging.getLogger(__name__)

def main():

    usage = "%prog [options] <input_dir> <output_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
            default=False, help="Be more verbose")
    parser.add_option('-m', '--move', dest='move', action='store_true',
            default=False, help="Instead of copying the files, the files "
            "will be moved to the destination. Default=False")
    parser.add_option('-a', '--aspect', dest='as_aspect', action='store_true',
            default=False, help='Instead of using the file resolution as '
            'folder name, use the aspect ration as folder name. For '
            'cross-platform compatibility, the generated names will use "@" '
            'instead of ":" as separator (f. ex.: 16@9) Default: not-set')

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.print_help()
        sys.exit(9)

    if options.verbose:
        print "Being verbose"
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    input_dir, output_dir = args

    move_files(input_dir, output_dir, options.as_aspect, move=options.move)
