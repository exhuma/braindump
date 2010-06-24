#!/usr/bin/python
"""
List disk usage sizes

Based on the example shown in the python documentation of "os.walk"
"""

import os
import sys
from os.path import join, getsize, isfile

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

def disk_usage( path, ignored_dirs=[] ):
   size = 0
   if isfile( path ):
      return getsize( path )

   for root, dirs, files in os.walk( path ):
      for name in files:
         try:
            size += getsize(join(root, name))
         except OSError, e:
            print "Unable to determine size for %r (%s)" % (join(root, name), str(e))

      for idir in ignored_dirs:
         if idir in dirs:
            dirs.remove(idir) # ignore this folder

   return size

def get_first_level_sizes( path ):
   """
   Determine the size for each folder and file in <path>
   """
   print "Calculating ..."
   output = []
   for entry in os.listdir(path):
      output.append( (join(path, entry), disk_usage( join(path, entry) )) )
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

   # remaining console width is filled with the progress bar
   bar_len = console_width - name_len - size_len - whitespace_len

   # sort results by occupied space
   sorted_results = sorted( results, cmp=lambda x, y: cmp(x[1], y[1]))

   # the string template for one line
   line_template = "%%-%ds %%%ds [%%-%ds]" % (name_len, size_len, bar_len)

   # for the progress bar
   max_size = sorted_results[-1][1]

   for root, size in sorted_results:
      pb_char_count = int(float(size) / max_size * bar_len)
      progress_bar = pb_char_count * "#"
      print line_template % (do_truncate and root[0:40] or root,
            human_readable(size),
            progress_bar)

def usage():
   print """
   Usage:
      %s <folder_name>
   """ % ( sys.argv[0] )

if __name__ == "__main__":

   if len( sys.argv ) < 2:
      usage()
      sys.exit(9)

   # pretty_print( get_size( sys.argv[1] ) )
   pretty_print( get_first_level_sizes( sys.argv[1] ) )

