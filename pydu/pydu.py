#!/usr/bin/python
"""
List disk usage sizes

Based on the example shown in the python documentation of "os.walk"
"""

import os
import sys
from os.path import join, getsize, isfile, islink, exists
from optparse import OptionParser

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

   if isfile( path ):
      try:
         return getsize( path )
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

def pretty_print( results, console_width=80 ):
   """
   Prints the folder sizes as a pretty console graph
   """
   if not results:
      return

   # determine the maximum length of folder names
   name_len = max([ len(x[0]) for x in results ])
   do_truncate = False
   if name_len > 40:
      print "WARNING: filename length exceeded maximum width. Truncating!"
      do_truncate = True
      name_len = 40

   # the width for the size number
   size_len = 10

   # the number of added whitespace
   whitespace_len  = 1 # the space after the path name
   whitespace_len += 1 # the space after the path size
   whitespace_len += 2 # the brackets around the prog. bar
   whitespace_len += 3 # the space and parens around the errors

   # the width of the "errors" text
   error_len = 9

   # remaining console width is filled with the progress bar
   bar_len = console_width - name_len - size_len - error_len - whitespace_len

   # sort results by occupied space
   sorted_results = sorted( results, cmp=lambda x, y: cmp(x[1], y[1]))

   # the string template for one line
   line_template = "%%-%ds %%%ds [%%-%ds] (err: %%4d)" % (name_len, size_len, bar_len)

   # for the progress bar
   max_size = sorted_results[-1][1]

   for root, size, errors in sorted_results:
      pb_char_count = int(float(size) / max_size * bar_len)
      progress_bar = pb_char_count * "#"
      print line_template % (do_truncate and root[0:40] or root,
            human_readable(size),
            progress_bar,
            errors)

def usage():
   print """
   Usage:
      %s <folder_name>
   """ % ( sys.argv[0] )

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
   for mountpoint in mounts.keys():
      if path.startswith( mountpoint ):
         return mounts[mountpoint]

if __name__ == "__main__":

   options, args = get_options()

   pretty_print( get_first_level_sizes( args[0], options ) )

   if not options.verbose:
      print "NOTE: Enabling the verbose flag will print errors '(err: xxx)' to stderr"

