Description
===========

Really simple module to decide wether a a date string is considered "obsolete"
or not.

Given a time-string like ``2010-01-01`` it will return ``True`` if this date
should *not* be retained, or ``False`` if it should.

Other time strings can be used by specifying a different format string (see
strftime_ and strptime_ for the detailed syntax)

Example Usage::

    from retaindate import is_obsolete
    from datetime import datetime, timedelta

    for i in range(10*365, -1, -1):
        date = datetime.today() - timedelta(i)
        if not is_obsolete(date):
            print date

More practical example (removing old backup files)::

    from retaindate import is_obsolete
    from os import listdir
    from os.path import abspath, join
    from datetime import datetime
    from time import strptime
    from subprocess import call
    import sys

    for line in listdir(sys.argv[1]):
        try:
            then = datetime(*strptime(line, '%Y-%m-%d')[0:6])
            if is_obsolete(then):
                path = join(abspath(sys.argv[1]), line)
                print "removing %s" % path
                call(['rm', '-rf', path])
        except ValueError:
            print >>sys.stderr, "Invalid date string: %r" % line

See the module docs (or the source) for more details

.. _strptime: http://docs.python.org/library/time.html#time.strptime
.. _strftime: http://docs.python.org/library/time.html#time.strftime
