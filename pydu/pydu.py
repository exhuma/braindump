#!/usr/bin/python
"""
List disk usage sizes

Based on the example shown in the python documentation of "os.walk"
"""

import os
import sys
from os.path import join, getsize, isfile, islink, isdir, exists, abspath
from optparse import OptionParser

TERM = None

## {{{ http://code.activestate.com/recipes/475116/ (r3)
import sys, re

class TerminalController:
    """
    A class that can be used to portably generate formatted output to
    a terminal.  
    
    `TerminalController` defines a set of instance variables whose
    values are initialized to the control sequence necessary to
    perform a given action.  These can be simply included in normal
    output to the terminal:

        >>> term = TerminalController()
        >>> print 'This is '+term.GREEN+'green'+term.NORMAL

    Alternatively, the `render()` method can used, which replaces
    '${action}' with the string required to perform 'action':

        >>> term = TerminalController()
        >>> print term.render('This is ${GREEN}green${NORMAL}')

    If the terminal doesn't support a given action, then the value of
    the corresponding instance variable will be set to ''.  As a
    result, the above code will still work on terminals that do not
    support color, except that their output will not be colored.
    Also, this means that you can test whether the terminal supports a
    given action by simply testing the truth value of the
    corresponding instance variable:

        >>> term = TerminalController()
        >>> if term.CLEAR_SCREEN:
        ...     print 'This terminal supports clearning the screen.'

    Finally, if the width and height of the terminal are known, then
    they will be stored in the `COLS` and `LINES` attributes.
    """
    # Cursor movement:
    BOL = ''             #: Move the cursor to the beginning of the line
    UP = ''              #: Move the cursor up one line
    DOWN = ''            #: Move the cursor down one line
    LEFT = ''            #: Move the cursor left one char
    RIGHT = ''           #: Move the cursor right one char

    # Deletion:
    CLEAR_SCREEN = ''    #: Clear the screen and move to home position
    CLEAR_EOL = ''       #: Clear to the end of the line.
    CLEAR_BOL = ''       #: Clear to the beginning of the line.
    CLEAR_EOS = ''       #: Clear to the end of the screen

    # Output modes:
    BOLD = ''            #: Turn on bold mode
    BLINK = ''           #: Turn on blink mode
    DIM = ''             #: Turn on half-bright mode
    REVERSE = ''         #: Turn on reverse-video mode
    NORMAL = ''          #: Turn off all modes

    # Cursor display:
    HIDE_CURSOR = ''     #: Make the cursor invisible
    SHOW_CURSOR = ''     #: Make the cursor visible

    # Terminal size:
    COLS = None          #: Width of the terminal (None for unknown)
    LINES = None         #: Height of the terminal (None for unknown)

    # Foreground colors:
    BLACK = BLUE = GREEN = CYAN = RED = MAGENTA = YELLOW = WHITE = ''
    
    # Background colors:
    BG_BLACK = BG_BLUE = BG_GREEN = BG_CYAN = ''
    BG_RED = BG_MAGENTA = BG_YELLOW = BG_WHITE = ''
    
    _STRING_CAPABILITIES = """
    BOL=cr UP=cuu1 DOWN=cud1 LEFT=cub1 RIGHT=cuf1
    CLEAR_SCREEN=clear CLEAR_EOL=el CLEAR_BOL=el1 CLEAR_EOS=ed BOLD=bold
    BLINK=blink DIM=dim REVERSE=rev UNDERLINE=smul NORMAL=sgr0
    HIDE_CURSOR=cinvis SHOW_CURSOR=cnorm""".split()
    _COLORS = """BLACK BLUE GREEN CYAN RED MAGENTA YELLOW WHITE""".split()
    _ANSICOLORS = "BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE".split()

    def __init__(self, term_stream=sys.stdout):
        """
        Create a `TerminalController` and initialize its attributes
        with appropriate values for the current terminal.
        `term_stream` is the stream that will be used for terminal
        output; if this stream is not a tty, then the terminal is
        assumed to be a dumb terminal (i.e., have no capabilities).
        """
        # Curses isn't available on all platforms
        try: import curses
        except: return

        # If the stream isn't a tty, then assume it has no capabilities.
        if not term_stream.isatty(): return

        # Check the terminal type.  If we fail, then assume that the
        # terminal has no capabilities.
        try: curses.setupterm()
        except: return

        # Look up numeric capabilities.
        self.COLS = curses.tigetnum('cols')
        self.LINES = curses.tigetnum('lines')
        
        # Look up string capabilities.
        for capability in self._STRING_CAPABILITIES:
            (attrib, cap_name) = capability.split('=')
            setattr(self, attrib, self._tigetstr(cap_name) or '')

        # Colors
        set_fg = self._tigetstr('setf')
        if set_fg:
            for i,color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, color, curses.tparm(set_fg, i) or '')
        set_fg_ansi = self._tigetstr('setaf')
        if set_fg_ansi:
            for i,color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, color, curses.tparm(set_fg_ansi, i) or '')
        set_bg = self._tigetstr('setb')
        if set_bg:
            for i,color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg, i) or '')
        set_bg_ansi = self._tigetstr('setab')
        if set_bg_ansi:
            for i,color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg_ansi, i) or '')

    def _tigetstr(self, cap_name):
        # String capabilities can include "delays" of the form "$<2>".
        # For any modern terminal, we should be able to just ignore
        # these, so strip them out.
        import curses
        cap = curses.tigetstr(cap_name) or ''
        return re.sub(r'\$<\d+>[/*]?', '', cap)

    def render(self, template):
        """
        Replace each $-substitutions in the given template string with
        the corresponding terminal control string (if it's defined) or
        '' (if it's not).
        """
        return re.sub(r'\$\$|\${\w+}', self._render_sub, template)

    def _render_sub(self, match):
        s = match.group()
        if s == '$$': return s
        else: return getattr(self, s[2:-1])

## end of http://code.activestate.com/recipes/475116/ }}}

def human_readable( size ):
   """
   Return a human-readable disk-size (B, kB, MB, GB)
   """
   if size < 1024:
      return "%d B" % size
   elif size < 1024**2:
      return "%1.2f kB" % (size/1024.0)
   elif size < 1024**3:
      return "%1.2f MB" % (size/1024.0**2)
   elif size < 1024**4:
      return "%1.2f GB" % (size/1024.0**3)

def disk_usage( path, ignored_dirs=[], verbose=False ):
   size = 0
   errors = 0
   path = abspath(path)

   if isfile( path ):
      try:
         return getsize( path ), 0
      except OSError, e:
         errors += 1
         if verbose:
            sys.stderr.write( "Unable to determine size for %r (%s)\n" % (
               join(root, name), str(e)) )
         return 0, errors

   for root, dirs, files in os.walk( path ):
      for name in files:
         try:
            size += getsize(join(root, name))
         except OSError, e:
            if verbose:
               sys.stderr.write( "Unable to determine size for %r (%s)\n" % (
                  join(root, name), str(e)) )
            errors += 1

      for idir in ignored_dirs:
         if idir in dirs:
            dirs.remove(idir) # ignore this folder

   return size, errors

def get_first_level_sizes( path, options ):
   """
   Determine the size for each folder and file in <path>
   """
   path = abspath( path )
   mounts = get_mounts()
   root_mp = get_mountpoint( path, mounts )

   print "Calculating ..."
   output = []
   for entry in os.listdir(path):
      entry_path = join(path,entry)
      entry_mp   = get_mountpoint( entry_path, mounts )

      # ignore files on different mountpoints (if enabled)
      if entry_mp['mountpoint'] != root_mp['mountpoint'] and options.one_fs:
         continue

      # ignore symbolic links unless forced
      if islink(entry_path) and not options.follow_symlinks:
         continue

      # ignore "virtual" mounts
      if entry_mp['device'] == 'none' and not options.include_virtual:
         continue

      du, errors = disk_usage( join(path, entry), verbose=options.verbose )
      output.append((
         entry_path,
         du,
         errors
         ))
   return output

def pretty_print( results ):
   """
   Prints the folder sizes as a pretty console graph
   """
   if not results:
      return

   # determine console width
   console_width = TERM.COLS or 80

   # minimum progress bar length
   bar_len_min = 5

   # the width for the size number
   size_len = 10

   # the number of added whitespace
   whitespace_len  = 1 # the space after the path name
   whitespace_len += 1 # the space after the path size
   whitespace_len += 2 # the brackets around the prog. bar
   whitespace_len += 3 # the space and parens around the errors

   # the width of the "errors" text
   error_len = 9

   # determine the maximum length of folder names
   name_len = max([ len(x[0]) for x in results ])
   name_len_max = console_width - bar_len_min - size_len - error_len - whitespace_len

   do_truncate = False
   if name_len > name_len_max:
      sys.stderr.write( "WARNING: filename length exceeded maximum width. Truncating!\n" )
      do_truncate = True
      name_len = name_len_max

   # remaining console width is filled with the progress bar
   bar_len = console_width - name_len - size_len - error_len - whitespace_len

   # sort results by occupied space
   sorted_results = sorted( results, cmp=lambda x, y: cmp(x[1], y[1]))

   # the string template for one line
   line_template = "%%s%%-%ds%%s %%%ds [%%-%ds] %%s(err: %%4d)%%s" % (name_len, size_len, bar_len)

   # for the progress bar
   max_size = sorted_results[-1][1]

   for root, size, errors in sorted_results:
      pb_char_count = int(float(size) / max_size * bar_len)
      progress_bar = pb_char_count * "#"
      print line_template % (
            isdir(root) and TERM.BLUE or TERM.NORMAL,
            do_truncate and root[0:name_len_max] or root,
            TERM.NORMAL,
            human_readable(size),
            progress_bar,
            errors and TERM.RED or TERM.NORMAL,
            errors,
            TERM.NORMAL
            )

def get_mounts():
   """
   Retrieve a list of mounted volumes
   So far, only available on linux
   """
   if not sys.platform.lower().startswith("linux"):
      raise UserWarning("Interface to mounted volumes is currently only" \
            " available on linux!")

   if not exists( "/proc/mounts" ):
      raise UserWarning("'/proc/mounts' not found!")

   mounts = open("/proc/mounts").readlines()
   output = {}
   for line in mounts:
      device, mountpoint, type, options, fsdump, fspass = line.strip().split()
      if type == "rootfs":
         # This seems "ignorable"
         continue

      output[mountpoint] = {
         "mountpoint": mountpoint,
         "device": device,
         "type": type,
         "options": options.split(","),
         "fsdump": fsdump,
         "fspass": fspass
      }

   return output

def get_options():
   usage  = "usage: %prog [options] <folder>"
   parser = OptionParser(usage=usage)
   parser.add_option( "-f", "--follow-symlinks", dest="follow_symlinks",
         help="Include symlinks in the report. By default, this is disabled.",
         default=False,
         action="store_true" )
   parser.add_option( "-1", "--one-fs", dest="one_fs", help="Ignore folders " \
         "which are mounted on other file systems. For example, if you "      \
         "report on '/' and '/home' is on a different fs, this option will "  \
         "prevent it being reported. By default, this is disabled",
         default=False,
         action="store_true" )
   parser.add_option( "-x", "--include-virtual", dest="include_virtual",
         help="Include virtual file systems. These are filesystems which "    \
              "have 'none' as mount device (for example: /dev and /proc). "   \
              "By default this is switched OFF",
              default=False,
              action="store_true")
   parser.add_option( "-v", "--verbose", dest="verbose",
         help="Print verbose output. Default is OFF",
         default=False,
         action="store_true")
   options, args = parser.parse_args()
   if not args:
      parser.print_usage()
      sys.exit(9)
   return (options, args)

def get_mountpoint( path, mounts ):
   """
   Returns the mountpoint of the specified folder

   @param path: The path
   @param mounts: A dictionary containing mount information (retrieve it with
                  get_mounts)
   """
   path = abspath(path)
   for mountpoint in mounts.keys():
      if path.startswith( mountpoint ):
         return mounts[mountpoint]

if __name__ == "__main__":

   TERM = TerminalController()
   options, args = get_options()

   pretty_print( get_first_level_sizes( args[0], options ) )

   if not options.verbose:
      print "NOTE: Enabling the verbose flag will print errors '(err: xxx)' to stderr"

