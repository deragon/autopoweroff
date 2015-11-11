# -*- coding: utf-8 -*-

import errno
import syslog
import os
import logging
from __main__ import scriptname,gTestMode,programname

#def disableFile():
#
#def enable(rundir):
  #cancelfile = rundir + "/" + scriptname + ".cancel"
  
logger = logging.getLogger(__name__)

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

def sendmsg(msg, logger=None, priority=syslog.LOG_INFO, tosyslog=True):
  # Ill attempt to use the stacktrace to determine the name of the logger.
  # But it is not viable.  For the moment, the code remains, commented,
  # in case one would like to retry again.
  #stacktrace=traceback.extract_stack()
  #print stacktrace
  if logger == None:
    logger = logging.getLogger(programname)
  logger.info(msg)
  if tosyslog:
    syslog.syslog(scriptname + ":  " + str(msg))

def commentString(text):
  regexp=re.compile("(?m)^")
  return regexp.sub("# ", text.rstrip().lstrip())

class APOCommand:

  # No enum used here as, of this writing, this code must remain
  # compatible with 2.x Python and we do not want to add a dependency
  # to module 'enum34'.
  #
  # See:  http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

  SHUTDOWN="shutdown"
  SLEEP="sleep"
  HIBERNATE="hibernate"
  OTHER="other"

  commands={}
  commands[SHUTDOWN]  = "/sbin/shutdown -h now"
  commands[SLEEP]     = "echo -n mem >/sys/power/state"
  commands[HIBERNATE] = "echo -n disk >/sys/power/state"

  def parse(string):
    if string == None:
       return None

    string = string.lower().strip()
    if string == APOCommand.SHUTDOWN    or \
       string == APOCommand.SLEEP       or \
       string == APOCommand.HIBERNATE:
      return string
    else:
      return None

  parse = staticmethod(parse)

class APOError(Exception):
  def __init__(self, header, lines, footer, errorcode):
    self.lines=lines.split("\n")
    self.header=header
    self.footer=footer
    self.errorcode=errorcode

    text=""
    for line in self.lines:
      text = text + "  - " + line + "\n"

    self.message = header + "\n\n" + text + "\n" + footer

  def __str__(self):
    return "Err #" + str(self.errorcode) + ":  " + self.message

class APOWarning(Exception):
  pass
