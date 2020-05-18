# -*- coding: utf-8 -*-

import errno
import syslog
import os
import logging
import pathlib
from __main__ import scriptname,gTestMode,programname

def createDirs(aDirs):
  for directory in aDirs:
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    # os.chmod(directory, 0o777)  # Used to be done, but not sure why it was
                                  # required.  Commented it out 2020-05-16.
                                  # Up to know, no problems founds without it.


def sendmsg(msg, logger=None, priority=syslog.LOG_INFO, tosyslog=True):
  # Ill attempt to use the stacktrace to determine the name of the logger.
  # But it is not viable.  For the moment, the code remains, commented,
  # in case one would like to retry again.
  #stacktrace=traceback.extract_stack()
  #print stacktrace
  if logger is None:
    logger = logging.getLogger(programname)
  logger.info(str(msg))
  if tosyslog:
    syslog.syslog(str(msg))


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
