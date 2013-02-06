from PIL import Image
from fractions import Fraction
import logging

LOG = logging.getLogger(__name__)

F_SIMPLE = 's'
F_ASPECT = 'a'
F_APPROX_ASPECT = 'x'

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

def simplify(numer, denom, approximate=False):
    """
    Simplifies the fraction, returning a tuple. If ``approximate`` is true,
    then the resulting fraction is only an approximation of the input number
    by limiting the denominator of the fraction to ``10``.

    :param numer: The numerator
    :param denom: The denominator
    :param approximate: Whether to approximate or not.
    """
    fract = Fraction(numer, denom)
    if approximate:
        fract = fract.limit_denominator(10)
    return fract.numerator, fract.denominator

def aspect_folder(width, height, format_=F_SIMPLE):
    """
    Given an image aspect ratio, return a folder name.

    :param format_: The folder naming format. One of :py:const:`F_SIMPLE`,
                   :py:const:`F_ASPECT` or :py:const:`F_APPROX_ASPECT`
    """
    if format_ == F_SIMPLE:
        return '{0}x{1}'.format(width, height)

    width, height = simplify(width, height,
            format_ in (F_ASPECT, F_APPROX_ASPECT))
    return "%d@%d" % (width, height)

def get_image_aspect(filepath, approximate=False):
    """
    Returns the image aspect ratio as a tuple of width/height. This simplifies
    the ratios as much as possible. Which may result in unexpected values.
    For example, instead of (16,10) it will return (8,5). But as this is the
    same value, you can use it as expected

    :param filepath: The filename
    :param approximate: Whether to approximate the size or not. See
                        :py:func:`simplify`
    """
    size = get_image_size(filepath)
    if not size:
        return None
    return simplify(*size, approximate=approximate)

def move_files(input_dir, output_dir, format_=F_SIMPLE, move=False):
    """
    Move files to the classification folders. The source folder is read *non*
    recursively!

    The names of the target folders depend on the ``format_`` value:

    * F_SIMPLE
      - A resolution of ``1600x1200`` goes to ``1600x1200``

    * F_ASPECT
      - A resolution of ``1600x1200`` goes to ``4@3``
      - A resolution of ``1920x1080`` goes to ``16@9``
      - A resolution of ``1920x1200`` goes to ``8@5`` (equivalent to
        ``16@10``)
      - A resolution of ``1554x1013`` goes to ``1554@1013``

    * F_APPROX_ASPECT
      - A resolution of ``1600x1200`` goes to ``4@3``
      - A resolution of ``1920x1080`` goes to ``16@9``
      - A resolution of ``1920x1200`` goes to ``8@5`` (equivalent to
        ``16@10``)
      - A resolution of ``1554x1013`` goes to ``14@9``. See
        :py:func:`simplify`

    :param input_dir: The directory containing the pictures.
    :param output_dir: The destination folder.
    :param format_: The directory naming scheme. Use one of
                    :py:const:`F_SIMPLE`, :py:const:`F_ASPECT` or
                    :py:const:`F_APPROX_ASPECT`
    """
    from os import listdir, makedirs
    from os.path import join, exists, dirname, basename
    from shutil import move as mv, copy2 as cp
    for filename in listdir(input_dir):
        in_file = join(input_dir, filename)
        clazz = None
        if format_ in (F_ASPECT, F_APPROX_ASPECT):
            approximate = format_ == F_APPROX_ASPECT
            aspect = get_image_aspect(in_file, approximate)
            if aspect:
                clazz = aspect_folder(*aspect, approximate=approximate)
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
