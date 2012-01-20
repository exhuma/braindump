from PIL import Image
from fractions import Fraction
import logging

LOG = logging.getLogger(__name__)

def get_image_size(filepath):
    """
    Returns a 2-tuple of the image dimensions. For example: (1024, 768)
    """
    try:
        im = Image.open(filepath)
        return im.size
    except Exception, e:
        LOG.error("Unable to open file %s (%s)" % (filepath, str(e)))
        return None

def get_image_aspect(filepath):
    """
    Returns the image aspect ratio as a tuple of width/height. This simplifies
    the rations as much as possible. Which may result in unexpected values.
    For example, instead of (16,10) it will return (8,5). But as this is the
    same value, you can use it as expected
    """
    size = get_image_size(filepath)
    if not size:
        return None
    x, y = size
    fract = Fraction(x, y)
    return fract.numerator, fract.denominator

def move_files(input_dir, output_dir, as_aspect=False, move=False):
    from os import listdir, makedirs
    from os.path import join, exists, dirname, basename
    from shutil import move as mv, copy2 as cp
    print as_aspect
    for filename in listdir(input_dir):
        in_file = join(input_dir, filename)
        clazz = None
        if as_aspect:
            aspect = get_image_aspect(in_file)
            if aspect:
                clazz = "%d@%d" % aspect
        else:
            size = get_image_size(in_file)
            if size:
                clazz = "%dx%d" % size

        if not clazz:
            LOG.error("Unable to determine output folder for %s" % in_file)
            continue
        target_folder = join(output_dir, clazz)
        if not exists(target_folder):
            makedirs(target_folder)
        out_file = join(target_folder, filename)

        operation = move and mv or cp
        op_text = move and "Moved" or "Copied"
        try:
            operation(in_file, out_file)
            LOG.info("%s %s to %s" % (op_text, basename(in_file),
                dirname(out_file)))
        except Exception, e:
            LOG.error(str(e))
