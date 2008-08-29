import errno
import syslog
import os
from __main__ import scriptname,testmode

def createDirs(aDirs):
  for directory in aDirs:
    try:
      # BUG.  os.makedirs() ignores the mode passed to it on Linux systems
      #       (or at least, on python 2.5.2, ubuntu 08.04).  We thus finish
      #       the work by setting the permission on the leaf by ourselves.
      os.makedirs(directory, 0777)
      os.chmod(directory, 0777)
    except OSError, oserror:
      # Error EEXIST (#17) is "File exists", which we ignore.  If anything
      # else, we raise it.
      if oserror[0] != errno.EEXIST:
        raise oserror

def sendmsg(msg, priority=syslog.LOG_INFO):
  print msg
  syslog.syslog(scriptname + ":  " + str(msg))

def debug(msg):
  if testmode:
    print msg

def commentString(text):
  regexp=re.compile("(?m)^")
  return regexp.sub("# ", text.rstrip().lstrip())
